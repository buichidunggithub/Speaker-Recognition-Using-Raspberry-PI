import sys
import os
import requests
import random

if len(sys.argv) != 4:
    print(sys.argv)
    sys.stderr.write("Usage: $0 <path-to-vivos> <dataset> <path-to-data-dir>\n")
    sys.stderr.write("e.g. $0 /export/vivos dev data/dev\n")
    sys.exit()

database = sys.argv[1]
dataset = sys.argv[2]
out_dir = sys.argv[3]

if dataset != "dev" and dataset != "test":
    sys.exit("dataset parameter must be 'dev' or 'test'")

if not os.path.exists(out_dir):
    try:
        os.makedirs(out_dir)
    except OSError as error:
        sys.exit("Error making directory {} with error: {}".format(out_dir, error))

print ("{}/{}/wav".format(database, dataset))
test_dir = os.path.join(database, dataset, "wav")

# try:
#     os.chdir(test_dir)
# except OSError as error:
#     sys.exit("Cannot open directory: {}".format(test_dir))
# print(os.getcwd())
print(os.listdir(test_dir))
# spk_dirs = [os.path.join(test_dir, dir) for dir in os.listdir(os.path.join(test_dir, ""))]
spk_dirs = [os.path.join(test_dir, dir) for dir in os.listdir(test_dir)]
def make_target_file():
    f = open(os.path.join(database, 'vivos_test.txt'), 'w')
    file_list = []
    for spkr_id in spk_dirs:
        id = spkr_id.split('/')[-1]
        # map[id] = []
        # rec_dirs = [os.path.join(dir, id) for id in os.listdir(dir)]
        # rec_dirs = os.listdir(spkr_id)
        # for rec_id in rec_dirs:
        files = os.listdir(spkr_id)  
        for file in files:
            wav = os.path.join(id, file)
            # print(wav)
            # map[id].append(wav)
            file_list.append(wav)
    for file1 in file_list:
        for file2 in file_list:
            # temp = random.randint(0, 1)
            # if temp == 1:
            id1 = file1.split('/')[0]
            id2 = file2.split('/')[0]
            # print(id1, id2)
            if id1 == id2:
                f.writelines('1 {} {}\n'.format(file1, file2))
            else:
                f.writelines('0 {} {}\n'.format(file1, file2))

    # return map


if dataset == "test":
    # if os.path.isfile(os.path.join(database, "vivos_test.txt")):
    #     print ("File exist")
    # else:
    #     print("File not")
    make_target_file()

    print(os.getcwd())
    trial_in = open(os.path.join(database, "vivos_test.txt"), "r")
    trial_out = open(os.path.join(out_dir, "trials"), "w")
    spkr_test = open(os.path.join(out_dir, "utt2spk"), "w")
    wav_test = open(os.path.join(out_dir, "wav.scp"), "w")

    test_spkrs = {}
    for trial in trial_in.readlines():
        trial = trial.strip()
        tar_or_non, path1, path2 = trial.split()
        spkr_id, name = path1.split('/')
        name = name.split('.')[0]
        utt_id1 = "{}-{}".format(spkr_id, name)
        # test_spkrs[spkr_id] = 

        spkr_id, name = path2.split('/')
        name = name.split('.')[0]
        utt_id2 = "{}-{}".format(spkr_id, name)

        target = "nontarget"
        if tar_or_non == "1":
            target = "target"

        # print(TRIAL_OUT "$utt_id1 $utt_id2 $target")
        trial_out.write("{} {} {}\n".format(utt_id1, utt_id2, target))

    for spkr_id in spk_dirs:
        # rec_dirs = [os.path.join(dir, id) for id in os.listdir(dir)]
        # rec_dirs = os.listdir(spkr_id)
        # for rec_id in rec_dirs:
        files = os.listdir(spkr_id)  
        for file in files:
            # print(os.path.join(spkr_id, rec_id, file))
            wav = os.path.join(spkr_id, file)
            # print(wav)
            name = wav.split(".")[0]
            name = name.split("/")[-1]
            id = spkr_id.split("/")[-1]
            utt_id = "{}-{}".format(id, name)
            wav_test.write("{} {}\n".format(utt_id, wav))
            spkr_test.write("{} {}\n".format(utt_id, id))


    spkr_test.close()
    wav_test.close()
    trial_in.close()
    trial_out.close()

    if os.system("utils/utt2spk_to_spk2utt.pl {}/utt2spk >{}/spk2utt".format(out_dir, out_dir)) != 0: 
        sys.exit("Error creating spk2utt file in directory {}".format(out_dir)) 

    os.system("env LC_COLLATE=C utils/fix_data_dir.sh {}".format(out_dir))
    if os.system("env LC_COLLATE=C utils/validate_data_dir.sh --no-text --no-feats {}".format(out_dir)) != 0: 
        sys.exit("Error validating directory {}".format(out_dir))










    