#!/usr/bin/env python3
"""
Basic tests for the meal planner project
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all main modules can be imported"""
    try:
        from app import calculate_target_nutrition, apply_health_restrictions
        print("✅ Main app functions imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import app functions: {e}")
        return False

def test_nutrition_calculation():
    """Test nutrition calculation logic"""
    from app import calculate_target_nutrition
    
    test_cases = [
        {'adjustedCalories': 2000, 'goal': 'Lose Weight'},
        {'adjustedCalories': 2500, 'goal': 'Build Muscle'},
        {'adjustedCalories': 3000, 'goal': 'Gain Weight'},
        {'adjustedCalories': 2200, 'goal': 'Maintain Weight'},
    ]
    
    for case in test_cases:
        result = calculate_target_nutrition(case)
        assert 'calories' in result
        assert 'protein' in result
        assert 'fat' in result
        assert 'carbs' in result
        assert result['calories'] == case['adjustedCalories']
    
    print("✅ All nutrition calculations passed")
    return True

if __name__ == "__main__":
    print("Running basic tests...")
    
    tests = [test_imports, test_nutrition_calculation]
    passed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {e}")
    
    print(f"\n🎯 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)