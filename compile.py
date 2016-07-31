import os
import sys
import bleach



import xml.etree.ElementTree as ET

# '/home/rodwan/Desktop/doctorate/ML/TIRA/codes/PAN16/'
# '/home/rodwan/Desktop/doctorate/ML/TIRA/codes/PAN16Compiled/'
# '/home/rodwan/Desktop/doctorate/ML/TIRA/codes/PAN16Tagged/'

def compile_files(source_folder):
    # get the list of files of the source_folder
    files = os.listdir(source_folder)

    i = 0
    # get a file at a time from the list
    for each_file in files:
        if each_file.endswith('.xml'):
            print(each_file)
            try:
               tree = ET.parse(source_folder+each_file)
               
            except:
                e = sys.exc_info()[0]
                print ("Filename: %s Error: %s" % (each_file, e))


            else:
                if not os.path.exists("compiled_dataset"):
                    os.makedirs("compiled_dataset")                
                fd = open("compiled_dataset/"+each_file[:-4]+'.txt','wb')
                root = tree.getroot()
                #a = []
                allText = "§i"
                for x in root.iter("document"):
                    #a.append(x.text)
                    clean = bleach.clean(x.text, tags=[], strip=True)
                    allText = allText + clean + "§f\n\n§i"

                allText = allText.encode('utf-8')

                fd.write(allText)
                #print(allText)
            fd.close();


def main(argv):

    source_folder = argv[0]
    #destiny_folder = argv[1]
    #compile_files(source_folder, destiny_folder)
    compile_files(source_folder+'/')



if __name__ == "__main__":
    main(sys.argv[1:])


