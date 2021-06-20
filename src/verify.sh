#!/usr/bin/env bash

. ./cmd.sh
. ./path.sh
set -e
rm -f trials
rm -f scores
rm -f results


nj=1

if [ $# != 1 ]; then
  echo "Usage: verify.sh <id> "
  echo " e.g.: verify.sh 001"
fi

id=$1
threshold=12.5

# Pretrained model
nnet_dir=exp/xvector_nnet_1a

stage=0

if [ $stage -le 0 ]; then
  # Create metadata for input
  python3 local/make_enroll.py input
  #g++ local/make_enroll.cpp  
  #./a.out input
 
fi

if [ $stage -le 1 ]; then
  # Make MFCCs and compute the energy-based VAD 
  mfccdir=input/mfcc
  vaddir=input/mfcc
  steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc.conf --nj $nj --cmd "$train_cmd" \
    input/feature exp/make_mfcc $mfccdir
  # utils/fix_data_dir.sh input/feature
  sid/compute_vad_decision.sh --nj $nj --cmd "$train_cmd" \
    input/feature exp/make_vad $vaddir
  # utils/fix_data_dir.sh input/feature
  
fi

# Extract x-vectors
if [ $stage -le 2 ]; then
  sid/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd --mem 1G" --nj $nj \
    $nnet_dir input/feature \
    input/xvector
fi


if [ $stage -le 3 ]; then
  # Create trial file
  echo "input-input $id-$id" > trials

  # Get score
  $train_cmd exp/scores/log/scoring.log \
    ivector-plda-scoring --normalize-length=true \
    "ivector-copy-plda --smoothing=0.0 $nnet_dir/xvectors_train/plda - |" \
    "ark:ivector-subtract-global-mean $nnet_dir/xvectors_train/mean.vec scp:input/xvector/xvector.scp ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    "ark:ivector-subtract-global-mean $nnet_dir/xvectors_train/mean.vec scp:db/${id}/xvector/xvector.scp ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- ark:- | ivector-normalize-length ark:- ark:- |" \
    trials scores  || exit 1;
fi

# Stage 12 cũ
if [ $stage -le 4 ]; then

  python3 local/get_result.py -f scores -t $threshold -r results

fi

