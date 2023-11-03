# create a new bucket where clients upload their audio recordings
gsutil mb gs://tonetrack_bucket


# internal bucket to store diarisation results
gsutil mb gs://tonetrack_diarisation_results