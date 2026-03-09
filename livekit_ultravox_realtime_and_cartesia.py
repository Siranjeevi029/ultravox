from livekit.agents import Agent, AgentSession, JobContext, JobProcess, WorkerOptions, cli
from livekit.plugins import silero, cartesia, deepgram
import os 
from livekit.plugins import ultravox

from livekit.plugins import openai
from dotenv import load_dotenv

load_dotenv(".env.local")

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    
    session: AgentSession[None] = AgentSession(
        # allow_interruptions=True,
        # vad=ctx.proc.userdata["vad"],
        llm=ultravox.realtime.RealtimeModel( output_medium="text"),
        tts=cartesia.TTS(
            model="sonic-3",
            voice="79a125e8-cd45-4c13-8a67-188112f4dd22",
            language="ta",
            
            
        ),
    )
    
    await session.start(
        agent=Agent(
            instructions="""
"You are a strict English-to-Tamil translation engine.Your ONLY task is to translate the given English input into Tamil.Rules (MUST FOLLOW STRICTLY):- Do NOT explain anything.- Do NOT add extra words.- Do NOT summarize.- Do NOT answer questions.- Do NOT change meaning.- Do NOT include notes, comments, or formatting.- Do NOT respond in English.- Output ONLY the Tamil translation.If the input is not in English, return it unchanged.Your response must contain ONLY the translated Tamil text and NOTHING ELSE"

            """,
            
        ),
        room=ctx.room,
    )

    await session.say("வணக்கம்! நான் உங்களுக்கு எப்படி உதவ முடியும்?")

def prewarm(proc: JobProcess) -> None:
    proc.userdata["vad"] = silero.VAD.load()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))