import sys
import os
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1

mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

def face_match(img_path, data_path): 

    img = Image.open(img_path)
    face, prob = mtcnn(img, return_prob=True)

    emb = resnet(face.unsqueeze(0)).detach()

    saved_data = torch.load(data_path)
    embedding_list = saved_data[0]
    name_list = saved_data[1]
    dist_list = []

    for idx, emb_db in enumerate(embedding_list):
        dist = torch.dist(emb, emb_db).item()
        dist_list.append(dist)

    idx_min = dist_list.index(min(dist_list))
    return (name_list[idx_min], min(dist_list))

if __name__ == "__main__":
    test_image = sys.argv[1]
    default_data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'data.pt')
    result = face_match(test_image, default_data_path)
    print(result[0])
