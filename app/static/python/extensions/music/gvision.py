import os


# from google.cloud import vision


# Google Vision API - Converts image into text
def detect_image(file_name):
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"
    ] = "./static/json/festive-freedom-309323-0124a1c976ae.json"
    client = vision.ImageAnnotatorClient()
    file_name = os.path.abspath(file_name)
    # Loads the image into memory
    with open(file_name, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Logos
    logo_list = []
    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    for logo in logos:
        logo_list.append(logo.description)

    if len(logo_list) > 0:
        return logo_list
    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    landmark_list = []
    for landmark in landmarks:
        landmark_list.append(landmark.description)

    if len(landmark_list) > 0:
        return landmark_list

    # General
    response = client.label_detection(image=image)
    labels = response.label_annotations
    general_list = []

    for label in labels:
        general_list.append(label.description)

    return general_list
