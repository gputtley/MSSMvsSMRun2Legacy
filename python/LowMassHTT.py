from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
import math

class LowMassHTT(PhysicsModel):
    def __init__(self):
        PhysicsModel.__init__(self)
        self.HggModel = False
        self.floatR = False

    def setPhysicsOptions(self, physOptions):
        for po in physOptions:
            if po.startswith("HggModel"):
                self.HggModel = True
            if po.startswith("floatR"):
                self.floatR = True

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        # --- POI and other parameters ----
            
        poiNames = []

        if self.HggModel:
          self.modelBuilder.doVar('mu[0,0,10]')
          poiNames.append('mu')
        elif self.floatR:
          self.modelBuilder.doVar('R[0.0619,0,1]')
          self.modelBuilder.doVar('mu[0,0,10]')
          poiNames.append('mu')
          poiNames.append('R')
        else:
          self.modelBuilder.doVar('muV[0,0,10]')
          self.modelBuilder.doVar('muggH[0,0,10]')
          poiNames.append('muV')
          poiNames.append('muggH')

        self.modelBuilder.doVar('muV_125[1,0,2]')
        self.modelBuilder.doVar('muggH_125[1,0,2]')
        self.modelBuilder.doVar('mutautau_125[1,0,2]')

        poiNames.append('muV_125')
        poiNames.append('muggH_125')
        poiNames.append('mutautau_125')

        self.modelBuilder.doSet('POI', ','.join(poiNames))

        params = {
                'ggh95_xs': 7.63E+01,
                'qqh95_xs': 5.034E+00,
                'h95_br': 8.32E-02,

                'ggh95_xs_th_uncert_up': 1.022,
                'ggh95_xs_th_uncert_down': 0.959,
                'qqh95_xs_th_uncert_up': 1.006,
                'qqh95_xs_th_uncert_down': 0.997,
                'ggh95_xs_pdf_uncert_up': 1.034,
                'ggh95_xs_pdf_uncert_down': 0.966,
                'qqh95_xs_pdf_uncert_up': 1.019,
                'qqh95_xs_pdf_uncert_down': 0.981,
                'h95_br_uncert_up': 1.0167,
                'h95_br_uncert_down': 0.9828,
        }

        if self.HggModel:
          # if using Hgg model scale XS and BR by the predictions for a 95 GeV SM Higgs
          # and then float signal by common rate parameter mu
          self.modelBuilder.factory_('expr::vbf95_scaling("@0*{h95_br}*{qqh95_xs}", mu)'.format(**params))
          self.modelBuilder.factory_('expr::ggh95_scaling("@0*{h95_br}*{ggh95_xs}", mu)'.format(**params))

          ## compute VBF ratio
          #vbf_ratio = params['qqh95_xs']/(params['qqh95_xs']+params['ggh95_xs']) 

          #vbf_ratio_vbf_th_uncert_up = params['qqh95_xs']*params['qqh95_xs_th_uncert_up']/(params['qqh95_xs']*params['qqh95_xs_th_uncert_up']+params['ggh95_xs']) / vbf_ratio
          #vbf_ratio_vbf_th_uncert_down = params['qqh95_xs']*params['qqh95_xs_th_uncert_down']/(params['qqh95_xs']*params['qqh95_xs_th_uncert_down']+params['ggh95_xs']) / vbf_ratio

          #vbf_ratio_vbf_pdf_uncert_up = params['qqh95_xs']*params['qqh95_xs_pdf_uncert_up']/(params['qqh95_xs']*params['qqh95_xs_pdf_uncert_up']+params['ggh95_xs']) / vbf_ratio
          #vbf_ratio_vbf_pdf_uncert_down = params['qqh95_xs']*params['qqh95_xs_pdf_uncert_down']/(params['qqh95_xs']*params['qqh95_xs_pdf_uncert_down']+params['ggh95_xs']) / vbf_ratio

          #vbf_ratio_ggh_th_uncert_up = params['qqh95_xs']/(params['qqh95_xs']+params['ggh95_xs']*params['ggh95_xs_th_uncert_up']) / vbf_ratio
          #vbf_ratio_ggh_th_uncert_down = params['qqh95_xs']/(params['qqh95_xs']+params['ggh95_xs']*params['ggh95_xs_th_uncert_down']) / vbf_ratio

          #vbf_ratio_ggh_pdf_uncert_up = params['qqh95_xs']/(params['qqh95_xs']+params['ggh95_xs']*params['ggh95_xs_pdf_uncert_up']) / vbf_ratio
          #vbf_ratio_ggh_pdf_uncert_down = params['qqh95_xs']/(params['qqh95_xs']+params['ggh95_xs']*params['ggh95_xs_pdf_uncert_down']) / vbf_ratio

          #print vbf_ratio
          #print vbf_ratio_vbf_th_uncert_up, vbf_ratio_vbf_th_uncert_down
          #print vbf_ratio_vbf_pdf_uncert_up, vbf_ratio_vbf_pdf_uncert_down

          #print vbf_ratio_ggh_th_uncert_up, vbf_ratio_ggh_th_uncert_down
          #print vbf_ratio_ggh_pdf_uncert_up, vbf_ratio_ggh_pdf_uncert_down

        elif self.floatR:
          # otherwise use seperate signal strength parameters for VBF and ggH which are both normalised to 1pb by default
          self.modelBuilder.factory_('expr::vbf95_scaling("@0*@1*{h95_br}*({ggh95_xs}+{qqh95_xs})", mu, R)'.format(**params))
          self.modelBuilder.factory_('expr::ggh95_scaling("@0*(1-@1)*{h95_br}*({ggh95_xs}+{qqh95_xs})", mu, R)'.format(**params))
        else:
          # otherwise use seperate signal strength parameters for VBF and ggH which are both normalised to 1pb by default
          self.modelBuilder.factory_('expr::vbf95_scaling("@0", muV)'.format(**params))
          self.modelBuilder.factory_('expr::ggh95_scaling("@0", muggH)'.format(**params))
        
        self.modelBuilder.factory_('expr::ggh125_scaling("@0*@1", muggH_125, mutautau_125)'.format(**params))
        self.modelBuilder.factory_('expr::qqh125_scaling("@0*@1", muV_125, mutautau_125)'.format(**params))

    def getYieldScale(self, bin_, process):

        scalings = []
        if 'ggH' in process and 'HWW' not in process and '125' in process:
          scalings.append('ggh125_scaling')
        if ('qqH' in process or 'WH' in process or 'ZH' in process) and 'HWW' not in process and '125' in process:
          scalings.append('qqh125_scaling')

        if 'ggX' in process and 'HWW' not in process and '125' not in process:
          scalings.append('ggh95_scaling')
        if 'qqX' in process and 'HWW' not in process and '125' not in process:
          scalings.append('vbf95_scaling')


        if scalings:
          scaling = '_'.join(scalings)
          print 'Scaling %s/%s as %s' % (bin_, process,scaling)
          return scaling
        else:
          return 1

LowMassHTT = LowMassHTT()


