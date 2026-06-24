from flask import Blueprint, request, jsonify, current_app
from app.services.whatsapp import WhatsAppService
from app.llm.router import LLMRouter
from app.rag.retriever import RAGService
from app.models import User, Message
from app import db
import logging

webhook_bp = Blueprint('webhook', __name__)
logger = logging.getLogger(__name__)

@webhook_bp.route('/', methods=['GET'], strict_slashes=False)
def verify():
    """WhatsApp webhook verification endpoint."""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == current_app.config['WHATSAPP_VERIFY_TOKEN']:
            logger.info("Webhook verified successfully")
            return challenge, 200
        else:
            logger.warning("Webhook verification failed: token mismatch")
            return 'Forbidden', 403
    return 'Bad Request', 400

@webhook_bp.route('/', methods=['POST'], strict_slashes=False)
def handle_message():
    """Handle incoming WhatsApp messages."""
    data = request.get_json()
    
    if not data or 'entry' not in data:
        return jsonify({"status": "ignored"}), 200

    try:
        entry = data['entry'][0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        
        if 'messages' in value:
            message_obj = value['messages'][0]
            whatsapp_number = message_obj.get('from')
            
            if 'text' in message_obj:
                user_text = message_obj['text']['body']
                logger.info(f"Received message from {whatsapp_number}")
                process_user_message(whatsapp_number, user_text)
            else:
                # Note: Media, images, voice, location etc. are Pro features
                logger.debug(f"Non-text message from {whatsapp_number} ignored (Pro feature)")
                # In Pro version: handle media and forward to CRM etc.
            
    except Exception as e:
        logger.exception(f"Error parsing webhook payload: {e}")

    # Always acknowledge to WhatsApp quickly
    return jsonify({"status": "success"}), 200

def process_user_message(whatsapp_number: str, user_text: str):
    """
    Core business logic: RAG retrieval + LLM generation + memory + reply.
    """
    # 1. Get or create user
    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        user = User(whatsapp_number=whatsapp_number)
        db.session.add(user)
        db.session.commit()
        logger.info(f"New user registered: {whatsapp_number}")

    # 2. Persist incoming user message
    user_msg = Message(user_id=user.id, role='user', content=user_text)
    db.session.add(user_msg)
    db.session.flush()  # get id without full commit yet

    # 3. RAG context retrieval
    rag_service = RAGService()
    context = rag_service.query(user_text)

    # 4. LLM
    llm_router = LLMRouter()
    llm = llm_router.get_llm()

    # Recent history for conversation continuity (last 6 messages)
    history_msgs = Message.query.filter_by(user_id=user.id)\
        .order_by(Message.timestamp.desc()).limit(6).all()
    history_text = "\n".join(
        [f"{m.role}: {m.content}" for m in reversed(history_msgs)]
    )

    prompt = f"""You are a helpful, concise AI assistant. 
Use ONLY the retrieved Context below to answer accurately. 
If the answer is not present in the context, say so clearly.

Context:
{context or "No relevant context found."}

Conversation History:
{history_text}

Current User Question: {user_text}

Answer:"""

    try:
        response = llm.invoke(prompt)
        ai_text = getattr(response, 'content', str(response))
    except Exception as e:
        logger.error(f"LLM error: {e}")
        ai_text = "Sorry, I ran into an issue generating a response. Please try again in a moment."

    # 5. Save AI response
    assistant_msg = Message(user_id=user.id, role='assistant', content=ai_text)
    db.session.add(assistant_msg)
    db.session.commit()

    # 6. Reply on WhatsApp
    whatsapp_service = WhatsAppService()
    whatsapp_service.send_message(whatsapp_number, ai_text)
