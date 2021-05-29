import sys
import os

#steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc.conf --nj $nj --cmd "$train_cmd" \
      #data/${name} exp/make_mfcc $mfccdir

if len(sys.argv) != 2:
    print(sys.argv)
    sys.stderr.write("Usage: $0 <speaker-dir>  \n")
    sys.stderr.write("e.g. $0 db/001 \n")
    sys.exit()
print(sys.argv)
database = sys.argv[1]
wav_dir = os.path.join(database, "wav")
out_dir = os.path.join(database, "feature")

if not os.path.exists(wav_dir):
    sys.exit("Error no wav file in {}\n".format(wav_dir))


if not os.path.exists(out_dir):
    try:
        os.makedirs(out_dir)
    except OSError as error:
        sys.exit("Error making directory {} with error: {}".format(out_dir, error))


# TODO: try catch thêm để phòng trường hợp ko có file hoặc nhiều hơn 1 file
# wav_file = os.listdir(wav_dir)[0]
spkr_id = database.split('/')[-1]
wav_file = spkr_id+".wav"
print('wav_file: ', wav_file)

spkr_test = open(os.path.join(out_dir, "utt2spk"), "w")
wav_test = open(os.path.join(out_dir, "wav.scp"), "w")


# spkr_id = database.split('/')[-1] # TODO: try catch them cho nay
utt_id = "{}-{}".format(spkr_id, spkr_id)
wav = os.path.join(wav_dir, wav_file)

wav_test.write("{} {}\n".format(utt_id, wav))
spkr_test.write("{} {}\n".format(utt_id, spkr_id))


spkr_test.close()
wav_test.close()


if os.system("utils/utt2spk_to_spk2utt.pl {}/utt2spk >{}/spk2utt".format(out_dir, out_dir)) != 0: 
    sys.exit("Error creating spk2utt file in directory {}".format(out_dir)) 

#os.system("env LC_COLLATE=C utils/fix_data_dir.sh {}".format(out_dir))
#if os.system("env LC_COLLATE=C utils/validate_data_dir.sh --no-text --no-feats {}".format(out_dir)) != 0: 
#    sys.exit("Error validating directory {}".format(out_dir))










    









    
