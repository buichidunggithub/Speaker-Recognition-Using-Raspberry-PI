#!/usr/bin/env bash



. ./cmd.sh
. ./path.sh
set -e


nj=1

if [ $# != 1 ]; then
  echo "Usage: extract.sh <id> "
  echo " e.g.: extract.sh 001"
fi

id=$1



# The trials file is downloaded by local/make_voxceleb1_v2.pl.
# trials=trials
# voxceleb1_root=export/corpora/VoxCeleb1_smaller
nnet_dir=exp/xvector_nnet_1a

stage=0

if [ $stage -le 0 ]; then
  # This script creates data/voxceleb1_test for latest version of VoxCeleb1.
  python3 local/make_enroll.py db/${id}  
  # local/make_voxceleb1_v2.pl $voxceleb1_root test data/voxceleb1_test
fi

if [ $stage -le 1 ]; then
  # Make MFCCs and compute the energy-based VAD for each dataset
  # for name in train voxceleb1_test; do
  mfccdir=db/${id}/mfcc
  vaddir=db/${id}/mfcc
  steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc.conf --nj $nj --cmd "$train_cmd" \
    db/${id}/feature exp/make_mfcc $mfccdir
  utils/fix_data_dir.sh db/${id}/feature
  sid/compute_vad_decision.sh --nj $nj --cmd "$train_cmd" \
    db/${id}/feature exp/make_vad $vaddir
  utils/fix_data_dir.sh db/${id}/feature
  
fi

# Extract x-vectors used in the evaluation.
if [ $stage -le 2 ]; then
  sid/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd --mem 4G" --nj $nj \
    $nnet_dir db/${id}/feature \
    db/${id}/xvector
fi



# # Stage 11 cũ
# if [ $stage -le 3 ]; then
#   $train_cmd exp/scores/log/voxceleb1_test_scoring.log \
#     ivector-plda-scoring --normalize-length=true \
#     "ivector-copy-plda --smoothing=0.0 $nnet_dir/xvectors_train/plda - |" \
#     "ark:ivector-subtract-global-mean $nnet_dir/xvectors_train/mean.vec scp:$nnet_dir/xvectors_voxceleb1_test/xvector.scp ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
#     "ark:ivector-subtract-global-mean $nnet_dir/xvectors_train/mean.vec scp:$nnet_dir/xvectors_voxceleb1_test/xvector.scp ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
#     "cat '$voxceleb1_trials' | cut -d\  --fields=1,2 |" exp/scores_voxceleb1_test || exit 1;
# fi

# # Stage 12 cũ

