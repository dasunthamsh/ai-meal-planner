import pytest
import numpy as np

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.genetic_algorithm import MealPlanGeneticAlgorithm

class TestGeneticAlgorithm:

    def test_initialization(self, sample_meal_data):
        """Test Genetic Algorithm initialization"""
        ga = MealPlanGeneticAlgorithm(sample_meal_data)

        assert ga.meals is not None
        assert ga.population == []
        assert ga.fitness_scores == []
        assert ga.best_solution is None
        assert ga.best_fitness == -float('inf')
        assert 'calories' in ga.nutrition_max

    def test_get_valid_meals(self, sample_meal_data):
        """Test getting valid meals based on restrictions"""
        ga = MealPlanGeneticAlgorithm(sample_meal_data)

        dietary_restrictions = {
            'vegetarian': True,
            'vegan': False,
            'allergies': [],
            'health_risks': []
        }

        valid_meals = ga._get_valid_meals(dietary_restrictions)

        assert isinstance(valid_meals, list)
        # Should only include vegetarian meals
        assert all(sample_meal_data.iloc[idx]['vegetarian'] == 1 for idx in valid_meals)

    def test_get_valid_meals_no_restrictions(self, sample_meal_data):
        """Test getting valid meals with no restrictions"""
        ga = MealPlanGeneticAlgorithm(sample_meal_data)

        dietary_restrictions = {
            'vegetarian': False,
            'vegan': False,
            'allergies': [],
            'health_risks': []
        }

        valid_meals = ga._get_valid_meals(dietary_restrictions)

        # Should include all meals when no restrictions
        assert len(valid_meals) == len(sample_meal_data)

    def test_initialize_population(self, sample_meal_data):
        """Test population initialization"""
        ga = MealPlanGeneticAlgorithm(sample_meal_data)

        dietary_restrictions = {
            'vegetarian': False,
            'vegan': False,
            'allergies': [],
            'health_risks': []
        }

        days = 3
        ga.initialize_population(days, dietary_restrictions)

        assert len(ga.population) > 0
        assert len(ga.population[0]) == days

        # Check each individual has correct structure
        for individual in ga.population:
            assert len(individual) == days
            for day_meals in individual:
                assert 'breakfast' in day_meals
                assert 'lunch' in day_meals
                assert 'dinner' in day_meals

    def test_calculate_fitness(self, sample_meal_data, target_nutrition, dietary_restrictions):
        """Test fitness calculation"""
        ga = MealPlanGeneticAlgorithm(sample_meal_data)

        # Create a simple individual
        individual = [
            {'breakfast': 0, 'lunch': 1, 'dinner': 2},
            {'breakfast': 0, 'lunch': 1, 'dinner': 2}
        ]

        fitness = ga.calculate_fitness(individual, target_nutrition, dietary_restrictions)

        assert isinstance(fitness, float)
        assert 0 <= fitness <= 1.0

    def test_tournament_selection(self, sample_meal_data, target_nutrition, dietary_restrictions):
        """Test tournament selection"""
        ga = MealPlanGeneticAlgorithm(sample_meal_data)
        ga.initialize_population(3, dietary_restrictions)

        # Calculate fitness scores first
        ga.fitness_scores = [
            ga.calculate_fitness(ind, target_nutrition, dietary_restrictions)
            for ind in ga.population
        ]

        parents = ga.tournament_selection()

        assert len(parents) == 2
        assert all(isinstance(parent, list) for parent in parents)

    def test_crossover(self, sample_meal_data):
        """Test crossover operation"""
        ga = MealPlanGeneticAlgorithm(sample_meal_data)

        parent1 = [
            {'breakfast': 0, 'lunch': 1, 'dinner': 2},
            {'breakfast': 0, 'lunch': 1, 'dinner': 2}
        ]

        parent2 = [
            {'breakfast': 3, 'lunch': 2, 'dinner': 1},
            {'breakfast': 3, 'lunch': 2, 'dinner': 1}
        ]

        child1, child2 = ga.crossover(parent1, parent2)

        assert len(child1) == len(parent1)
        assert len(child2) == len(parent2)

    def test_mutate(self, sample_meal_data, dietary_restrictions):
        """Test mutation operation"""
        ga = MealPlanGeneticAlgorithm(sample_meal_data)

        individual = [
            {'breakfast': 0, 'lunch': 1, 'dinner': 2},
            {'breakfast': 0, 'lunch': 1, 'dinner': 2}
        ]

        mutated = ga.mutate(individual, dietary_restrictions)

        assert len(mutated) == len(individual)
        assert isinstance(mutated, list)
