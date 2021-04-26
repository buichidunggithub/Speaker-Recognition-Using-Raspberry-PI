#!/usr/bin/env bash



. ./cmd.sh
. ./path.sh
set -e


nj=1

if [ $# != 1 ]; then
  echo "Usage: verify.sh <id> "
  echo " e.g.: verify.sh 001"
fi

id=$1



# The trials file is downloaded by local/make_voxceleb1_v2.pl.
# trials=trials
# voxceleb1_root=export/corpora/VoxCeleb1_smaller
nnet_dir=exp/xvector_nnet_1a

stage=0

if [ $stage -le 0 ]; then
  # This script creates data/voxceleb1_test for latest version of VoxCeleb1.
  python3 local/make_enroll.py input
  # local/make_voxceleb1_v2.pl $voxceleb1_root test data/voxceleb1_test
fi

if [ $stage -le 1 ]; then
  # Make MFCCs and compute the energy-based VAD for each dataset
  # for name in train voxceleb1_test; do
  mfccdir=input/mfcc
  vaddir=input/mfcc
  steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc.conf --nj $nj --cmd "$train_cmd" \
    input/feature exp/make_mfcc $mfccdir
  utils/fix_data_dir.sh input/feature
  sid/compute_vad_decision.sh --nj $nj --cmd "$train_cmd" \
    input/feature exp/make_vad $vaddir
  utils/fix_data_dir.sh input/feature
  
fi

# Extract x-vectors used in the evaluation.
if [ $stage -le 2 ]; then
  sid/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd --mem 4G" --nj $nj \
    $nnet_dir input/feature \
    input/xvector
fi



# Stage 11 cũ
if [ $stage -le 3 ]; then
  $train_cmd exp/scores/log/scoring.log \
    ivector-plda-scoring --normalize-length=true --verbose=10 \
    "ivector-copy-plda --smoothing=0.0 $nnet_dir/xvectors_train/plda - |" \
    "ark:ivector-subtract-global-mean $nnet_dir/xvectors_train/mean.vec scp:input/xvector/xvector.scp ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "ark:ivector-subtract-global-mean $nnet_dir/xvectors_train/mean.vec scp:db/${id}/xvector/xvector.scp ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    trials exp/scores_voxceleb1_test  || exit 1;
fi

# Stage 12 cũ

