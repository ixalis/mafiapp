from engine.models import *

# Should be called only after all players have been added.
def initialize_standard_conditions(game):
	_generate_on_day_start(game)
	_generate_on_day_end(game)

	players = Player.objects.filter(game=game)
	for p in players:
		_generate_on_death(p)

		for p2 in players:
			_generate_on_kill(killer, victim)

def _generate_on_death(player):
	name = player.user.username + "-died"
	description = "Triggers when " + player.user.username + " dies."
	on_death = Condition(name=name, game=player.game, description=description)
	on_death.save()

def _generate_on_kill(killer, victim):
	name = killer.user.username + "-killed-" + victim.user.username
	description = "Triggers when " + killer.user.username + " kills " + victim.user.username + "."
	on_kill = Condition(name=name, game=killer.game, description=description)
	on_kill.save()

def _generate_on_day_start(game):
	on_day_start = Condition(name="on-day-start", game=game, description="Triggers on day start.")
	on_day_start.save()

def _generate_on_day_end(game):
	on_day_end = Condition(name="on-day-end", game=game, description="Triggers on day end.")
	on_day_end.save()



# Should be called only for items that can be used.
def generate_on_use(item):
	name = item.name + "-used"
	description = "Triggers when " + item.name + " is used."
	on_use = Condition(name=name, game=item.game, description=description)
	on_use.save()