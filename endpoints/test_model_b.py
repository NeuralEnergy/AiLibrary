

from basic_inference_server import FlaskWorker


_CONFIG = {
  'WEIGHT'    : 1,
  'BIAS'      : 2,
}

class TestModelBWorker(FlaskWorker):

  """
  Example implementation of a worker

  Obs: as the worker runs on thread, then no prints are allowed; use `_create_notification` and see all the notifications
       when calling /notifications of the server.
  """

  def __init__(self, **kwargs):
    super(TestModelBWorker, self).__init__(prefix_log='[DUMB]', **kwargs)
    return


  def _load_model(self):
    ### see docstring in parent
    ### abstract method implementation: no model to be loaded
    return

  def _pre_process(self, inputs):
    ### see docstring in parent
    ### abstract method implementation: parses the request inputs and keep the value for 'INPUT_VALUE'
    if 'INPUT_VALUE' not in inputs.keys():
      raise ValueError('INPUT_VALUE should be defined in inputs')
    weight = inputs.get('WEIGHT') or self.cfg_weight
    bias = inputs.get('BIAS') or self.cfg_bias
    s = float(inputs['INPUT_VALUE']), weight, bias
    return s

  def _predict(self, prep_inputs):
    ### see docstring in parent
    ### abstract method implementation: "in-memory model :)" that adds and subtracts.
    val, weight, bias = prep_inputs
    self._create_notification(
      notif='log',
      msg='Predicting on usr_input: {} using {}'.format(prep_inputs, self.config_data)
    )
    res = '{}*{} + {} = {} PREDICTED'.format(val, weight, bias, val * weight + bias)
    return res

  def _post_process(self, pred):
    ### see docstring in parent
    ### abstract method implementation: packs the endpoint answer that will be jsonified
    return {
      'dummy_model_predict' : pred, 
      'description' : 'Neural Energy inference test endpoint #2',
    }
