# The NLC2CMD competition@NeurIPS 2020   

[Competition Link](http://nlc2cmd.us-east.mybluemix.net/)   
----------------------------------------------------------------------
## Training models
1. Install libraries: `pytorch`, `fairseq`    
`pip install -r requirements.txt`   
2. Download [NL2Bash data](https://ibm.box.com/v/nl2bash-data) and [AInix data](https://github.com/DNGros/ai-nix-kernal-dataset-archie-json/blob/master/ainix-kernal-dataset-archie.json) in `train/data` directory   
3. Setup submodule [TellinaTool](https://github.com/TellinaTool/nl2bash/tree/master)
`./0.setup_submodule.sh`
4. Convert the file format of AInix   
`./1.convert_ainix_data.sh`
(make a sh file for doing 2, 3, and 4 at once)   
5. Run preprocess   
`./2.preprocess.sh`   
6. Train template predictor   
`./3.train_template_predictor.sh`   
7. Train argument predictor   
`./4.train_argument_predictor.sh`   
