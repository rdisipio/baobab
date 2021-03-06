# author: Riccardo Di Sipio <disipio@cern.ch>

GeV = 1e3
TeV = 1e6
mH   = 125.0 * GeV
mtop = 172.5 * GeV

iLumi15 = 3193.68
iLumi16 = 568.47
iLumi = iLumi15 + iLumi16

############################################
# SYSTEMATICS

systematics_leptons  = [
]

systematics_btagging  = [
   "bTagSF_77_eigenvars_B_up_0",
   "bTagSF_77_eigenvars_B_down_0",
   "bTagSF_77_eigenvars_B_up_1",
   "bTagSF_77_eigenvars_B_down_1",
   "bTagSF_77_eigenvars_B_up_2",
   "bTagSF_77_eigenvars_B_down_2",
   "bTagSF_77_eigenvars_B_up_3",
   "bTagSF_77_eigenvars_B_down_3",
   "bTagSF_77_eigenvars_B_up_4",
   "bTagSF_77_eigenvars_B_down_4",
   "bTagSF_77_eigenvars_B_up_5",
   "bTagSF_77_eigenvars_B_down_5",
   "bTagSF_77_eigenvars_C_up_0",
   "bTagSF_77_eigenvars_C_down_0",
   "bTagSF_77_eigenvars_C_up_1",
   "bTagSF_77_eigenvars_C_down_1",
   "bTagSF_77_eigenvars_C_up_2",
   "bTagSF_77_eigenvars_C_down_2",
   "bTagSF_77_eigenvars_C_up_3",
   "bTagSF_77_eigenvars_C_down_3",
   "bTagSF_77_eigenvars_Light_up_0",
   "bTagSF_77_eigenvars_Light_down_0",
   "bTagSF_77_eigenvars_Light_up_1",
   "bTagSF_77_eigenvars_Light_down_1",
   "bTagSF_77_eigenvars_Light_up_2",
   "bTagSF_77_eigenvars_Light_down_2",
   "bTagSF_77_eigenvars_Light_up_3",
   "bTagSF_77_eigenvars_Light_down_3",
   "bTagSF_77_eigenvars_Light_up_4",
   "bTagSF_77_eigenvars_Light_down_4",
   "bTagSF_77_eigenvars_Light_up_5",
   "bTagSF_77_eigenvars_Light_down_5",
   "bTagSF_77_eigenvars_Light_up_6",
   "bTagSF_77_eigenvars_Light_down_6",
   "bTagSF_77_eigenvars_Light_up_7",
   "bTagSF_77_eigenvars_Light_down_7",
   "bTagSF_77_eigenvars_Light_up_8",
   "bTagSF_77_eigenvars_Light_down_8",
   "bTagSF_77_eigenvars_Light_up_9",
   "bTagSF_77_eigenvars_Light_down_9",
   "bTagSF_77_eigenvars_Light_up_10",
   "bTagSF_77_eigenvars_Light_down_10",
   "bTagSF_77_eigenvars_Light_up_11",
   "bTagSF_77_eigenvars_Light_down_11",
   "bTagSF_77_eigenvars_Light_up_12",
   "bTagSF_77_eigenvars_Light_down_12",
   "bTagSF_77_eigenvars_Light_up_13",
   "bTagSF_77_eigenvars_Light_down_13",
   "bTagSF_77_extrapolation_up",
   "bTagSF_77_extrapolation_down",
   "bTagSF_77_extrapolation_from_charm_up",
   "bTagSF_77_extrapolation_from_charm_down",
]

weight_systematics = systematics_btagging + systematics_leptons

