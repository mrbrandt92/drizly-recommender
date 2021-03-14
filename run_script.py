import os

os.system("docker image build --no-cache -t drizly_recommender . ; "
          "docker run -p 8080:8081 -d drizly_recommender")