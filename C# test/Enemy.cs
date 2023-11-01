using System;

struct Enemy
{
    public string name;
    public string race;
    public int life;
    public int attack;
    public string modifyer;
    public int armor;
    public int loot;

    public void dump()
    {
        Console.WriteLine($"Name: {name}, Race: {race}, Life: {life}, Attack: {attack}, Modifyer: {modifyer}, Armor: {armor}, Loot: {loot}");
    }
}