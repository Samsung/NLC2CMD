fairseq-preprocess \
--source-lang nl \
--target-lang cm \
--trainpref corpus/template_predictor/train \
--validpref corpus/template_predictor/valid \
--testpref corpus/template_predictor/test \
--destdir src/submission_code/template_predictor \
--joined-dictionary

CUDA_VISIBLE_DEVICES=0 fairseq-train src/submission_code/template_predictor \
--save-dir checkpoints/template_predictor \
--tensorboard-logdir logs/template_predictor \
--max-tokens 4096 \
--arch transformer \
--encoder-layers 2 --decoder-layers 2 \
--encoder-embed-dim 256 --decoder-embed-dim 256 \
--encoder-ffn-embed-dim 1024 --decoder-ffn-embed-dim 1024 \
--encoder-attention-heads 8 --decoder-attention-heads 8 \
--encoder-normalize-before --decoder-normalize-before \
--weight-decay 0.0 \
--optimizer adam --adam-betas '(0.9, 0.998)' --clip-norm 0.0 \
--lr-scheduler inverse_sqrt --warmup-init-lr 0.000008 --warmup-updates 100 \
--lr 0.0005 --min-lr 1e-09 \
--max-epoch 600 \
--keep-last-epochs 1 \
--save-interval 100 \
--fp16 \
--update-freq 4 \
--criterion cross_entropy \
--share-all-embeddings

