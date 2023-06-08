def makeTextFile(name, content):
    """
    Function to create a text file and write the content into it.

    Args:
        name (str): The name of the file to be created.
        content (str): The content to be written into the file.
    """

    # Open the file in write mode
    file = open(f"../youtube-transcript-summarizer-frontend/src/transcripts/{name}.txt", "w", encoding="utf-8")
    
    # Write the name and content into the file
    file.write(f"{name} Transcript:\n")
    file.write(content)

    # Close the file
    file.close()
