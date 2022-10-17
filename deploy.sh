#!/bin/bash
fission spec init
fission env create --spec --name suita-profile-update-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name suita-profile-update-fn --env suita-profile-update-env --src "./func/*" --entrypoint main.update_suitability_profile --executortype newdeploy --maxscale 1
fission route create --spec --name suita-profile-update-rt --method PUT --url /onboarding/set_suitability --function suita-profile-update-fn