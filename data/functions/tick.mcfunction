# Gives an id to every item that doesn't already have an id
execute if score #loaded picarrow.iid.item_id matches 1 as @e[type=minecraft:item] unless score @s picarrow.iid.item_id = @s picarrow.iid.item_id at @s run function picarrow.item_id:assess
