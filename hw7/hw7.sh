#!/bin/sh

./hw7_dist_similarity.sh 2 FREQ mc_similarity.txt hw7_sim_2_FREQ_output.txt
./hw7_dist_similarity.sh 2  PMI mc_similarity.txt hw7_sim_2_PMI_output.txt
./hw7_dist_similarity.sh 10 PMI mc_similarity.txt hw7_sim_10_PMI_output.txt
./hw7_cbow_similarity.sh 2      mc_similarity.txt hw7_sim_2_CBOW_output.txt
