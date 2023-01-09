fission spec init
fission env create --spec --name acc-suit-quest-update-env --image nexus.sigame.com.br/fission-account-suit-quest-update:0.1.2 --poolsize 0 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name acc-suit-quest-update-fn --env acc-suit-quest-update-env --code fission.py --targetcpu 80 --executortype newdeploy --maxscale 3 --requestsperpod 10000 --spec
fission route create --spec --name acc-suit-quest-update-rt --method PUT --url /suitability/profile_update --function acc-suit-quest-update-fn