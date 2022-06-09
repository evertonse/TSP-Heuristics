from collections import Counter
class MultiSet(Counter):
	def __init__(self, *args, **kargs):
		super().__init__(*args,**kargs)
		
		self._size = 0
		for i in self:
			self._size += self[i]
			
	def add(self,item):
		self[item] +=1
		self._size +=1

	def remove(self,item):
		self[item] -=1
		self._size -=1
		if self[item] <=0:
			del(self[item])

	def __len__(self) -> int:
		return self._size
	
	def __iter__(self):
		iterable_list = list()
		for item in super().__iter__():
			for _ in range(self[item]):
				if item is not None:
					iterable_list.append(item)
		return iter(iterable_list) 
	
	def __repr__(self) -> str:
		return f"mset{tuple(self.__iter__())}"
	
	def __hash__(self):
		return hash(tuple(sorted(list(self.__iter__()))))
	

