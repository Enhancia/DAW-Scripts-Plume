try:
    from .Neova import Neova
except ImportError:
    from Neova import Neova

def create_instance(c_instance):
	return Neova(c_instance)