import os
from uuid import uuid4
import streamlit as st
from openai import OpenAI
from firecrawl import FirecrawlApp
from elevenlabs.client import ElevenLabs
from elevenlabs import save

# Streamlit UI setup
st.set_page_config(page_title="📰 ➡️ 🎙️ Blog to Podcast", page_icon="🎙️")
st.title("📰 ➡️ 🎙️ Blog to Podcast")

# Sidebar: API Keys
st.sidebar.header("🔑 API Keys")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
firecrawl_api_key = st.sidebar.text_input("Firecrawl API Key", type="password")

# Check if all keys are provided
keys_provided = all([openai_api_key, elevenlabs_api_key, firecrawl_api_key])

# Blog URL input
url = st.text_input("Enter the blog URL:", "")

# Button
generate_button = st.button("🎙️ Generate Podcast", disabled=not keys_provided)

if not keys_provided:
    st.warning("Please enter all required API keys to proceed.")

if generate_button:
    if not url.strip():
        st.warning("Please enter a valid blog URL.")
    else:
        with st.spinner("Scraping, summarizing, and generating podcast..."):
            try:
                # Step 1: Scrape blog content using Firecrawl
                firecrawl = FirecrawlApp(api_key=firecrawl_api_key)
                result = firecrawl.scrape_url(url, formats=["markdown"])

                # Debug: see what we actually got
                st.write(f"Result type: {type(result)}")
                st.write(f"Result attributes: {dir(result)}")

                # Try different ways to access the content
                if hasattr(result, 'markdown'):
                    blog_text = result.markdown
                elif hasattr(result, 'data') and isinstance(result.data, dict):
                    blog_text = result.data.get("markdown", "")
                else:
                    blog_text = str(result)  # fallback

                if not blog_text:
                    st.error("Failed to extract blog content.")
                    st.stop()

                # Step 2: Summarize with OpenAI
                client = OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You're a podcast script writer."},
                        {"role": "user", "content": f"Summarize this blog in under 2000 characters in a conversational tone:\n\n{blog_text}"}
                    ]
                )

                summary = response.choices[0].message.content.strip()
                if len(summary) > 2000:
                    summary = summary[:2000]

                # Step 3: Generate audio with ElevenLabs v1
                eleven = ElevenLabs(api_key=elevenlabs_api_key)

                audio = eleven.text_to_speech.convert(
                    text=summary,
                    voice_id="JBFqnCBsd6RMkjVDRZzb",
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128"
                )

                filename = f"audio_generations/podcast_{uuid4()}.mp3"
                os.makedirs("audio_generations", exist_ok=True)
                save(audio, filename)

                # Step 4: Streamlit playback and download
                st.success("Podcast generated successfully! 🎧")
                
                # Read the file with proper error handling
                try:
                    with open(filename, "rb") as f:
                        audio_bytes = f.read()
                    
                    # Add some debugging info
                    st.write(f"Audio file size: {len(audio_bytes)} bytes")
                    
                    # Try HTML audio element instead of st.audio()
                    import base64
                    audio_b64 = base64.b64encode(audio_bytes).decode()
                    audio_html = f"""
                    <div style="margin: 20px 0;">
                        <h4>🎧 Your Podcast:</h4>
                        <audio controls style="width: 100%;">
                            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                    """
                    st.markdown(audio_html, unsafe_allow_html=True)
                    
                    # Also try st.audio as backup
                    st.write("Alternative player:")
                    st.audio(audio_bytes, format="audio/mp3")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Podcast",
                        data=audio_bytes,
                        file_name="generated_podcast.mp3",
                        mime="audio/mp3"
                    )
                    
                except Exception as file_error:
                    st.error(f"Error reading audio file: {file_error}")
                    # Still provide download even if playback fails
                    try:
                        with open(filename, "rb") as f:
                            audio_bytes = f.read()
                        st.download_button(
                            label="📥 Download Podcast",
                            data=audio_bytes,
                            file_name="generated_podcast.mp3",
                            mime="audio/mp3"
                        )
                    except:
                        st.error("Could not read audio file for download.")

            except Exception as e:
                st.error(f"An error occurred: {e}")