import argparse
import generate_corpora.generate_intentions as generate_intentions
import generate_corpora.check_is_illegal as check_is_illegal
import os
def runner():
    parser = argparse.ArgumentParser()
    base_dir = os.getcwd()
    parser.add_argument('--base', default=base_dir, type=str)
    parser.add_argument("--tag", default="./data/tags.txt", type=str)
    parser.add_argument("--ptr", default="./data/patterns.txt", type=str)
    parser.add_argument("--target", default="./data/final.csv", type=str)
    args = parser.parse_args()
    ptr_file = args.base+"/"+args.ptr
    tag_file = args.base+"/"+args.tag
    target_file = args.base+"/"+args.target
    tag, ptr = generate_intentions.read_files(ptr_file, tag_file)
    check_is_illegal.check(ptr)
    generate_intentions.extend_existing_items(ptr)

    with open(target_file, 'w', encoding="utf8") as f:
        #        fwriter = csv.writer(f, delimiter=',',
        #                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        separator = '|'
        for key, item in ptr.items():
            if key is not None:
                s = generate_intentions.gen_sentences(item, tag)
                s_saved = separator.join(generate_intentions.flatten(s))
                f.writelines([key+','+s_saved+'\n'])
                #fwriter.writerow([ptr[k], s_saved])
    print("Succeed to generating corpora in ./data/final.csv!")

if __name__ == "__main__":
    runner()
