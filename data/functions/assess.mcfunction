tag @s add picarrow.iid.assessing
data modify storage picarrow.item_id:0 Item set from entity @s Item
execute as @e[type=minecraft:armor_stand,x=0.5,y=-70,z=0.5,distance=..0.00001,tag=picarrow.iid.helper,limit=1] run function picarrow.item_id:assess_1
tag @s remove picarrow.iid.assessing
tellraw @a {"score":{"name":"@s","objective":"picarrow.iid.item_id"}}
