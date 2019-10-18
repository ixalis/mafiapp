from engine.models import *

# Should be called only after all players have been added.
def initialize_standard_items(game, mafia, sks):
	_generate_status_alive(game)
	_generate_lynch_vote(game)
	_generate_mafia_kill(game, mafia)
	for sk in sks:
		_generate_sk_kill(sk)

def _generate_status_alive(game):
	status_alive = Item(game=game, name="status-alive")
	status_alive.save()
	players = Player.objects.filter(game=game)
	for p in players:
		status_alive.owners.add(p)

def _generate_lynch_vote(game):
	lynch_vote = Item(game=game, name="lynch-vote")
	lynch_vote.save()
	players = Player.objects.filter(game=game)
	for p in players:
		lynch_vote.owners.add(p)

def _generate_mafia_kill(game, mafia):
	mafia_kill = Item(game=game, name="mafia-kill")
	mafia_kill.save()
	for m in mafia:
		mafia_kill.owners.add(m)

def _generate_sk_kill(game, sk):
	sk_kill = Item(game=game, name="sk-kill")
	sk_kill.save()
	sk_kill.owners.add(sk)



def generate_status_guilty(killer, victim):
	name = "status-guilty-" + victim.user.username
	status_guilty = Item(game=game, name=name)
	status_guilty.save()
	status_guilty.owners.add(killer)

def generate_status_roleblocked(player):
	status_roleblocked = Item("status-roleblocked")
	status_roleblocked.save()
	status_roleblocked.add(player)