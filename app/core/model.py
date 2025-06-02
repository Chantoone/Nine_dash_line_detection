import torch
import torchvision
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.models import vgg16, VGG16_Weights
from torchvision.transforms import functional as F
from PIL import Image
import os
from app.core.config import MODEL_PATH, CONFIDENCE_THRESHOLD,MODEL_50_PATH
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
class NineDashLineDetector:
    def __init__(self, model_path=MODEL_PATH):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._load_model(model_path)
        self.model.eval()
        self.model.to(self.device)    
    def _load_model(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Không tìm thấy file mô hình tại: {model_path}")
          
        def create_backbone():
            weights = VGG16_Weights.DEFAULT
            model = vgg16(weights=weights)
            backbone = model.features
            for param in list(backbone.parameters())[:10]:
                param.requires_grad = False
            backbone.out_channels = 512
            return backbone
        def create_faster_rcnn(num_classes):
            backbone = create_backbone()
            rpn_anchor_generator = AnchorGenerator(
                sizes=((32,64,128,256,512,1028),),
                aspect_ratios=((0.5,1.0,2.0),)
            )
            roi_pooler = torchvision.ops.MultiScaleRoIAlign(
                featmap_names=['0'],
                output_size=7,
                sampling_ratio=2
            )
            model = FasterRCNN(
                backbone,
                num_classes=num_classes,
                rpn_anchor_generator=rpn_anchor_generator,
                box_roi_pool=roi_pooler
            )
            return model
        
        model = create_faster_rcnn(2)
        
        try:
            checkpoint = torch.load(model_path, map_location=self.device)
            model.load_state_dict(checkpoint, strict=False)
            print("Model loaded successfully with non-strict matching")
        except Exception as e:
            print(f"Warning when loading model: {str(e)}")
            print("Continuing with initialized model")
        
        return model
    
    def detect(self, image_path):

        image = Image.open(image_path).convert("RGB")

        img_tensor = F.to_tensor(image).to(self.device)

        with torch.no_grad():
            predictions = self.model([img_tensor])

        result = {
            "detected": False,
            "detections": []
        }
        
        boxes = predictions[0]['boxes'].cpu().numpy()
        scores = predictions[0]['scores'].cpu().numpy()

        for box, score in zip(boxes, scores):
            if score >= CONFIDENCE_THRESHOLD:
                result["detected"] = True
                result["detections"].append({
                    "box": box.tolist(),
                    "confidence": float(score)
                })
        
        return result

_detector = None


class NineDashLineDetectorV2:
    def __init__(self, model_path=MODEL_50_PATH):

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._load_model(model_path)
        self.model.eval()
        self.model.to(self.device)


    def _load_model(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Không tìm thấy file mô hình tại: {model_path}")

        def create_faster_rcnn_resnet50(num_classes):

            model = fasterrcnn_resnet50_fpn(weights="DEFAULT")

            in_features = model.roi_heads.box_predictor.cls_score.in_features
            model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

            for name, param in model.backbone.body.named_parameters():
                if "layer4" not in name:
                    param.requires_grad = False
            return model

        model = create_faster_rcnn_resnet50(2)


        checkpoint = torch.load(model_path,map_location=self.device)
        model.load_state_dict(checkpoint)

        return model

    def detect(self, image_path):

        image = Image.open(image_path).convert("RGB")

        img_tensor = F.to_tensor(image).to(self.device)

        with torch.no_grad():
            predictions = self.model([img_tensor])

        result = {"detected": False,
            "detections": []
        }

        boxes = predictions[0]['boxes'].cpu().numpy()
        scores = predictions[0]['scores'].cpu().numpy()

        for box, score in zip(boxes, scores):
            if score >= CONFIDENCE_THRESHOLD:
                result["detected"] = True
                result["detections"].append({
                    "box": box.tolist(),
                    "confidence": float(score)
                })

        return result

_detector=None
def get_detector():
    global  _detector
    if _detector is None:
        _detector = NineDashLineDetector()
    return _detector
