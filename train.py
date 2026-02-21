from ultralytics import YOLO

def main():
    # 1. Load a pre-trained YOLOv8 'Small' model
    # It will automatically download the base weights the first time you run this
    print("Loading base model...")
    model = YOLO("yolov8s.pt") 

    # 2. Train the model on your custom dataset
    print("Starting training...")
    results = model.train(
        data="yoloDataset/data.yaml", # Path to your configured yaml file
        epochs=50,                    # Number of times it will loop through your data
        imgsz=640,                    # Standard image resolution for training
        batch=16,                     # How many images it processes at once
        device=0,                     # Explicitly forces it to use your NVIDIA GPU
        project="Capstone_Model",     # Main folder where results are saved
        name="EcoSort_v1",            # Subfolder for this specific run
        plots=True                    # Generates accuracy graphs automatically
    )
    
    print("Training finished successfully!")

# This block is strictly required on Windows to prevent multi-threading crash errors
if __name__ == '__main__':
    main()