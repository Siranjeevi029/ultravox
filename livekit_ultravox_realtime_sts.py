from livekit.agents import AgentSession, Agent, JobContext, WorkerOptions, cli
from livekit.plugins import ultravox
from dotenv import load_dotenv

load_dotenv(".env.local")


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    # ✅ ONLY Ultravox (no VAD, no STT, no TTS)
    session = AgentSession(
        llm=ultravox.realtime.RealtimeModel(
            output_medium="voice",  # 🔥 IMPORTANT
        ),
    )

    await session.start(
        agent=Agent(
            instructions=
"""
You are a strict English-to-Tamil translation engine.

Your ONLY task is to translate the given English input into Tamil.

Rules (MUST FOLLOW STRICTLY):
- Do NOT explain anything.
- Do NOT add extra words.
- Do NOT summarize.
- Do NOT answer questions.
- Do NOT change meaning.
- Do NOT include notes, comments, or formatting.
- Do NOT respond in English.
- Output ONLY the Tamil translation.

If the input is not in English, return it unchanged.

Your response must contain ONLY the translated Tamil text and NOTHING ELSE.
            """
            
        ),
        room=ctx.room,
    )

    # 🔥 This will stream audio directly
    # await session.say("வணக்கம்! நான் உங்களுக்கு எப்படி உதவ முடியும்?")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint)
    )