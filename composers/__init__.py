__version__ = 0.1


'''

Classes must return a stuct 
{
	metadata:{
	},
	patterns:{
	
	},
	song:[
	   ... list of patterns
	]
}

'''
from alphabet import alphabet
class twotones(  ) :
	def generatePiece(self):

		empty  = []
		circle = [[0,0],[300,0],[300,300],[0,300],[0,0]]
		square = [[0,0],[-300,0],[-300,-300],[0,-300],[0,0]]
		patterns = alphabet
		patterns [' '] = []		
		patterns ['empty'] = None		
		string = "R";
		song = []
		for letter in string :
			for i in range(20):
				song.append( letter )
			for i in range(2):
				song.append('empty')

		self.content = {
			"metadata" : {
			},
			"patterns" : patterns,
			"song" : song
		}
		return self

		"""
						'empty','empty','empty','empty',
				'A','A','A','A','A','A','A','A',
				'empty','empty','empty','empty',
				'B','B','B','B','B','B','B','B',
				'empty','empty','empty','empty',
				'C','C','C','C','C','C','C','C',
				'empty','empty','empty','empty',
				'D','D','D','D','D','D','D','D',
				'empty','empty','empty','empty',
				'E','E','E','E','E','E','E','E',
				'empty','empty','empty','empty',
				'F','F','F','F','F','F','F','F',
				'empty','empty','empty','empty',
				
				'empty','empty','empty','empty',

				"""