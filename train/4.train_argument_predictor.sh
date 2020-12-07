fairseq-preprocess \
--source-lang ctx \
--target-lang arg \
--trainpref corpus/argument_predictor/train \
--validpref corpus/argument_predictor/valid \
--testpref corpus/argument_predictor/test \
--destdir src/submission_code/argument_predictor \
--joined-dictionary

CUDA_VISIBLE_DEVICES=0 fairseq-train src/submission_code/argument_predictor \
--save-dir checkpoints/argument_predictor \
--tensorboard-logdir logs/argument_predictor \
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
--update-freq 4 \
--fp16 \
--criterion cross_entropy \
--share-all-embeddings

