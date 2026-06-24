from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class LLMRouter:
    """
    Intelligent multi-provider LLM router with graceful fallback.
    
    Priority order:
    1. Groq (fast & cheap Llama3)
    2. Google Gemini
    3. OpenAI
    4. xAI Grok (via OpenAI compatible if key present)
    5. Anthropic Claude
    """

    def __init__(self):
        self.config = current_app.config

    def get_llm(self):
        """Return the first available configured LLM client."""
        # 1. Groq
        if self.config.get('GROQ_API_KEY'):
            try:
                logger.info("Initializing Groq LLM")
                return ChatGroq(
                    temperature=0,
                    model_name="llama-3.3-70b-versatile",
                    groq_api_key=self.config['GROQ_API_KEY']
                )
            except Exception as e:
                logger.warning(f"Groq initialization failed: {e}")

        # 2. Gemini
        if self.config.get('GOOGLE_API_KEY'):
            try:
                logger.info("Falling back to Gemini")
                return ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    google_api_key=self.config['GOOGLE_API_KEY']
                )
            except Exception as e:
                logger.warning(f"Gemini initialization failed: {e}")

        # 3. OpenAI
        if self.config.get('OPENAI_API_KEY'):
            try:
                logger.info("Falling back to OpenAI")
                return ChatOpenAI(
                    model_name="gpt-4o-mini",
                    openai_api_key=self.config['OPENAI_API_KEY']
                )
            except Exception as e:
                logger.warning(f"OpenAI initialization failed: {e}")

        # 4. xAI Grok - use OpenAI-compatible endpoint if langchain supports via base_url in future
        if self.config.get('XAI_API_KEY'):
            try:
                logger.info("Falling back to xAI (Grok)")
                # Note: As of 2026 xAI may have native or OpenAI compatible client.
                # Using ChatOpenAI with base_url override is one common pattern.
                return ChatOpenAI(
                    model_name="grok-2-latest",
                    openai_api_key=self.config['XAI_API_KEY'],
                    openai_api_base="https://api.x.ai/v1"
                )
            except Exception as e:
                logger.warning(f"xAI initialization failed: {e}")

        # 5. Claude
        if self.config.get('ANTHROPIC_API_KEY'):
            try:
                logger.info("Falling back to Claude")
                return ChatAnthropic(
                    model_name="claude-3-5-sonnet-20240620",
                    anthropic_api_key=self.config['ANTHROPIC_API_KEY']
                )
            except Exception as e:
                logger.error(f"Claude initialization failed: {e}")

        raise ValueError("No LLM providers available or configured correctly. Please set at least one *_API_KEY.")
