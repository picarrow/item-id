# Keeps our helper alive and loaded
forceload add 0 0
execute unless entity @e[type=minecraft:armor_stand,x=0.5,y=-70,z=0.5,distance=..0.00001,tag=picarrow.iid.helper,limit=1] run summon minecraft:armor_stand 0.5 -70 0.5 {Tags:[picarrow.iid.helper],Marker:1b,Invisible:1b}

# Tracks system flags, temporary variables, and the ids of items
scoreboard objectives add picarrow.iid.item_id dummy
scoreboard players set #loaded picarrow.iid.item_id 1
