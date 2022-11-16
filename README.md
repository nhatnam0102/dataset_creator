# upc_yolov5_dataset_creator
Build 
```cmd
pyinstaller .\main.py -p .\ui:.\utils:.\widget --add-data=".\data;.\data" --add-data=".\image_process;.\image_process" --add-data=".\dataset;.\dataset" --add-data=".\constants.py;." -n DatasetGenerator -w
```

