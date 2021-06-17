import os
import argparse

# python run_low_mass_limits.py -o low_mass

parser = argparse.ArgumentParser()
parser.add_argument('--channel',help= 'Channel to run limits for', default='all')
parser.add_argument('--output','-o', help= 'Name of output directory', default='output')
parser.add_argument('--year', help= 'Name of input year', default='all')
parser.add_argument('--all_perm', help= 'Run all permutations of year and channel inputs', default=False)
args = parser.parse_args()

channel = args.channel
output = args.output
year = args.year
all_perm = args.all_perm

analysis = 'low_mass'

if all_perm:
  if channel == 'fake':
    channel_perm = ['et','mt','tt','fake']
  elif channel == 'all':
    channel_perm = ['em','et','mt','tt','all']
  else:
    channel_perm = channel.split(",").append(channel)

  if year == 'all':
    year_perm = ['2016','2017','2018','all']
  else:
    year_perm = year.split(',').append(year)
else:
  channel_perm = [channel]
  year_perm = [year]
    

for year in year_perm:
  for channel in channel_perm:
    ### Set up channel input ###
    if channel == "all":
      cat_file = 'low_mass_categories.txt'
    elif channel == "fake":
      cat_file = 'low_mass_categories.txt'
    elif channel in ["et","tt","mt","em"]:
      cat_file = 'low_mass_%(channel)s_categories.txt' % vars() # need to create these files is you want to use this option
    
    ### Set up year input ###
    if year == "all":
      year_text = "2016,2017,2018"
      year_list = ["2016","2017","2018"]
    else:
      year_text = year
      year_list = year.split(",")
      
    
    ### Datacard creation ###
    dc_creation_cmd = 'morph_parallel.py --output model_independent_limits/%(output)s_%(channel)s_%(year)s --analysis "%(analysis)s" --eras %(year_text)s --category_list input/%(cat_file)s --variable "nnscore" --sm_gg_fractions data/higgs_pt_reweighting_fullRun2.root --parallel 5 --additional_arguments="--auto_rebin=1"' % vars()
    print dc_creation_cmd
    os.system(dc_creation_cmd)
    
    directory = "model_independent_limits/%(output)s_%(channel)s_%(year)s_%(analysis)s" % vars()
    
    for yr in year_list:
      os.system("mkdir -p %(directory)s/%(yr)s/cmb/; rsync -av --progress %(directory)s/%(yr)s/htt_*/*  %(directory)s/%(yr)s/cmb/" % vars())
    os.system("mkdir -p %(directory)s/combined/cmb/; rsync -av --progress %(directory)s/201?/htt_*/*  %(directory)s/combined/cmb/" % vars())
    
    ### Workspace creation ###
    
    os.system("ulimit -s unlimited")
    os.system('combineTool.py -m 95 -M T2W -P CombineHarvester.MSSMvsSMRun2Legacy.LowMassHTT:LowMassHTT -i %(directory)s/combined/cmb -o ws_Hgg.root --parallel 8 --PO HggModel' % vars())
    os.system('combineTool.py -m 95 -M T2W -P CombineHarvester.MSSMvsSMRun2Legacy.LowMassHTT:LowMassHTT -i %(directory)s/combined/cmb -o ws.root --parallel 8' % vars()) 
    os.system('combineTool.py -m 95 -M T2W -P CombineHarvester.MSSMvsSMRun2Legacy.LowMassHTT:LowMassHTT -i %(directory)s/combined/cmb -o ws_floatR.root --parallel 8 --PO floatR ' % vars()) 

    # float R

    os.system('combineTool.py -m 95 -M Significance --freezeParameters=M95_XS_ratio,muggH_125,muV_125,mutautau_125 --setParameters mu=0.5,muV_125=1,muggH_125=1,mutautau_125=1,R=0.061 --redefineSignalPOIs mu   -d %(directory)s/combined/cmb/ws_floatR.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 -t -1 -n .floatR.freezeH125 ' % vars())

    os.system('combineTool.py -m 95 -M Significance --freezeParameters=M95_XS_ratio,mutautau_125 --setParameters mu=0.5,muV_125=1,muggH_125=1,mutautau_125=1,R=0.061 --redefineSignalPOIs mu   -d %(directory)s/combined/cmb/ws_floatR.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 -t -1 -n .floatR.floatH125 ' % vars())

    os.system('combineTool.py -m 95 -M Significance --freezeParameters=M95_XS_ratio,muggH_125,muV_125 --setParameters mu=0.5,muV_125=1,muggH_125=1,mutautau_125=1,R=0.061 --redefineSignalPOIs mu   -d %(directory)s/combined/cmb/ws_floatR.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 -t -1 -n .floatR.floatIncH125 ' % vars())

    # Hgg model - R fixed to SM value

    os.system('combineTool.py -m 95 -M Significance --freezeParameters=muggH_125,muV_125,mutautau_125 --setParameters mu=0.5,muV_125=1,muggH_125=1,mutautau_125=1 --redefineSignalPOIs mu   -d %(directory)s/combined/cmb/ws_Hgg.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 -t -1 -n .HggModel.freezeH125 ' % vars())
 
    os.system('combineTool.py -m 95 -M Significance --freezeParameters=mutautau_125 --setParameters mu=0.5,muV_125=1,muggH_125=1,mutautau_125=1 --redefineSignalPOIs mu   -d %(directory)s/combined/cmb/ws_Hgg.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 -t -1 -n .HggModel.floatH125 ' % vars()) 
    
    os.system('combineTool.py -m 95 -M Significance --freezeParameters=muggH_125,muV_125 --setParameters mu=0.5,muV_125=1,muggH_125=1,mutautau_125=1 --redefineSignalPOIs mu   -d %(directory)s/combined/cmb/ws_Hgg.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 -t -1 -n .HggModel.floatIncH125 ' % vars()) 
    
    os.system('combineTool.py -m 95 -M Significance --freezeParameters=M95_XS_ratio,muggH_125,muV_125 --setParameters muV=0.21,muggH=3.17,muV_125=1,muggH_125=1,mutautau_125=1 --redefineSignalPOIs muV,muggH   -d %(directory)s/combined/cmb/ws.root --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 -t -1  -n .TwoProcModel.floatIncH125 ' % vars()) 
 
 
    ### Run model-independent limits ###

    #os.system('combineTool.py -m "95" -M AsymptoticLimits --rAbsAcc 0 --rRelAcc 0.0005 --boundlist input/mssm_boundaries.json --setParameters r_ggH=0,r_bbH=0 --redefineSignalPOIs r_ggH -d %(directory)s/combined/cmb/ws.root --there -n ".ggH" --task-name ggH_full_combined_%(analysis)s_%(channel)s_%(year)s_%(output)s --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.01 -v 1 --job-mode \'SGE\' --prefix-file ic --sub-opts "-q hep.q -l h_rt=3:0:0" ' % vars())

    #os.system('combineTool.py -m "95" -M AsymptoticLimits --rAbsAcc 0 --rRelAcc 0.0005 --boundlist input/mssm_boundaries.json --setParameters r_ggH=0,r_bbH=0 --redefineSignalPOIs r_bbH -d %(directory)s/combined/cmb/ws.root --there -n ".bbH" --task-name bbH_full_combined_%(analysis)s_%(channel)s_%(year)s_%(output)s --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.01 -v 1 --job-mode \'SGE\' --prefix-file ic --sub-opts "-q hep.q -l h_rt=3:0:0" ' % vars())
    

