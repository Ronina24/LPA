import altair as alt
import pandas as pd
import logging
from LPA import PCA, Corpus, sockpuppet_distance
import sys


def main(freq_file_path,metadata):

    sig_length_metadata = int(metadata['signature'])
    #threshold_metadata = float(metadata['threshold'])
    logging.basicConfig(filename='progress_log.txt', level=logging.INFO, 
                        format='%(asctime)s %(levelname)s:%(message)s')

    alt.data_transformers.disable_max_rows()
    
    logging.info("1.Reading frequency data...")
    freq = pd.read_csv(freq_file_path)
    
    logging.info("2. Creating DVR from the corpus...")
    corpus = Corpus(freq=freq, name='Corpus')
    dvr = corpus.create_dvr()
    logging.info("DVR created.")
    
    epsilon_frac = 2
    epsilon = 1 / (len(dvr) * epsilon_frac)
    logging.info(f"Epsilon calculated: {epsilon}")

    print("Creating signatures of length: ", sig_length_metadata)
    signatures = corpus.create_signatures(epsilon=epsilon, sig_length=sig_length_metadata, distance="KLDe")
    logging.info("Signatures created.")


    print("Calculating sockpuppet distance with signature length of: ",sig_length_metadata)
    spd = sockpuppet_distance(corpus, corpus)
    spd = spd.drop_duplicates(subset='value', keep='first').sort_values(by='value',ascending=True)
    logging.info(f"Sockpuppet distance calculated {spd}")
    filtered_spd = spd.sort_values(by='value', ascending=True)
    filtered_spd.columns = ['Corpus 1', 'Corpus 2', 'value']    
    print("Finished calculate sockpuppet distance- check results file in the results bucket")
    return filtered_spd


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py <freq_file_path>")
        sys.exit(1)
    freq_file_path = sys.argv[1]
    metadata = sys.argv[2]
    main(freq_file_path,metadata)