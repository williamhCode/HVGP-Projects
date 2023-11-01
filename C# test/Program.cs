using System;

namespace C__test
{
    class Program
    {

        static void Main(string[] args)
        {
            Enemy enemy_1 = new Enemy() {name = "Raider", race = "Humanoid", life = 4, attack = 1, modifyer = "Pierce", armor = 1, loot = 10};
            Enemy enemy_2 = new Enemy() {name = "Gremlin", race = "Monsteu", life = 4, attack = 1, modifyer = "Slash", armor = 0, loot = 0};
            Enemy enemy_3 = new Enemy() {name = "Orc Shaman", race = "Humanoid", life = 5, attack = 1, modifyer = "Arcane", armor = 2, loot = 0};
            Enemy enemy_4 = new Enemy() {name = "Orc Warrior", race = "Humanoid", life = 10, attack = 1, modifyer = "Arcane", armor = 2, loot = 0};
            Enemy enemy_5 = new Enemy() {name = "Orc Warrior", race = "Humanoid", life = 10, attack = 1, modifyer = "Arcane", armor = 2, loot = 0};

            Console.WriteLine();
            enemy_1.dump();
            enemy_2.dump();
            enemy_3.dump();
            enemy_4.dump();
            Console.WriteLine();
        }
    }
}
