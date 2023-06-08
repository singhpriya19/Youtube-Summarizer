from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript_of_yt_video(v_id):
    """
    Function to retrieve the transcript of a YouTube video using the YouTube Transcript API.

    Args:
        v_id (str): The YouTube video ID.

    Returns:
        list or str: A list of dictionaries representing the transcript if available,
                    or '0' if the transcript is not available.
    """

    try:
        # Retrieve the list of available transcripts for the video
        transcript_list = YouTubeTranscriptApi.list_transcripts(v_id)
        l = len(list(transcript_list))

        if l > 1:
            try:
                # Get the transcript in English language
                final_transcript = YouTubeTranscriptApi.get_transcript(v_id, languages=['en'])
                return final_transcript
            except:
                for i in transcript_list:
                    start_with = str(i)[:2]
                    # Find and translate the transcript to English
                    transcript = transcript_list.find_transcript([start_with])
                    final_transcript = transcript.translate('en').fetch()
                    return final_transcript
        else:
            for i in transcript_list:
                start_with = str(i)[:2]
                if start_with == 'en':
                    # Get the transcript in English language
                    final_transcript = YouTubeTranscriptApi.get_transcript(v_id, languages=['en'])
                else:
                    # Find and translate the transcript to English
                    transcript = transcript_list.find_transcript([start_with])
                    final_transcript = transcript.translate('en').fetch()
                return final_transcript

    except:
        # Return '0' if the transcript is not available
        final_transcript = "0"
        return final_transcript
