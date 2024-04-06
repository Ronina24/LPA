import altair as alt
import pandas as pd
import logging
from LPA import PCA, Corpus, sockpuppet_distance


def main():
    logging.basicConfig(filename='progress_log.txt', level=logging.INFO, 
                        format='%(asctime)s %(levelname)s:%(message)s')

    alt.data_transformers.disable_max_rows()
    
    logging.info("1.Reading frequency data...")
    freq = pd.read_csv('test_data/test_freq.csv')

    logging.info("  Data loaded successfully.")
    
    logging.info("2. Creating DVR from the corpus...")
    corpus = Corpus(freq=freq, name='Corpus')
    dvr = corpus.create_dvr()
    logging.info("DVR created.")
    
    epsilon_frac = 2
    epsilon = 1 / (len(dvr) * epsilon_frac)
    logging.info(f"Epsilon calculated: {epsilon}")

    logging.info("Creating signatures...")
    signatures = corpus.create_signatures(epsilon=epsilon, sig_length=500, distance="KLDe")
    logging.info("Signatures created.")


    logging.info("Calculating sockpuppet distance...")
    spd = sockpuppet_distance(corpus, corpus)
    logging.info(f"Sockpuppet distance calculated {spd}")
    filtered_spd = spd[spd['value'] > 0].sort_values(by='value', ascending=True)
    # print(spd)
    print(filtered_spd)
    #num_rows = filtered_spd.shape[0]  
    #print(f"Number of rows in the filtered DataFrame: {num_rows}")
    with open("filtered_data_stats.txt", "w") as stats_file:
        num_rows = filtered_spd.shape[0]
        stats_file.write(f"Number of rows in the filtered DataFrame: {num_rows}\n")


    logging.info("E - N - D")

event = {
    "key1": "value1",
    "key2": "value2"
}

# Define a sample context
class Context:
    def __init__(self):
        self.aws_request_id = "123456789"
        self.log_group_name = "/aws/lambda/my-function"
        # Define other context attributes as needed

context = Context()

if __name__ == '__main__':
    main()