
from unittest import TestCase
from unittest import mock
from freesurfer_pp_moc.freesurfer_pp_moc import Freesurfer_pp_moc


class Freesurfer_pp_mocTests(TestCase):
    """
    Test Freesurfer_pp_moc.
    """
    def setUp(self):
        self.app = Freesurfer_pp_moc()

    def test_run(self):
        """
        Test the run code.
        """
        args = []
        if self.app.TYPE == 'ds':
            args.append('inputdir') # you may want to change this inputdir mock
        args.append('outputdir')  # you may want to change this outputdir mock

        # you may want to add more of your custom defined optional arguments to test
        # your app with
        # eg.
        # args.append('--custom-int')
        # args.append(10)

        options = self.app.parse_args(args)
        self.app.run(options)

        # write your own assertions
        self.assertEqual(options.outputdir, 'outputdir')
