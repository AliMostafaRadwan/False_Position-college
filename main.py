import streamlit as st
import pandas as pd
import numpy as np
from sympy import symbols, sympify, lambdify

def false_position(f, a, b, tol):
    if f(a) * f(b) >= 0:
        return None, "Function has the same sign at points a and b."
    
    data = []
    while True:
        X = ((a*f(b))-(b*f(a))) / (f(b) - f(a))
        data.append((a, b, X, f(X), abs(b-a)))
        
        if abs(f(X)) < tol:
            return pd.DataFrame(data, columns=["a", "b", "X", "f(x)", "Error"]), None
        
        if f(a) * f(X) < 0:
            b = X
        else:
            a = X

def main():
    st.title("False Position Method Calculator")

    # User input for the function, interval, and tolerance
    user_function = st.text_area("Enter the function f(x):", value="x**4 - 3*x**2 - 3")
    a = st.number_input("Enter the value for a (interval start):", value=1.0)
    b = st.number_input("Enter the value for b (interval end):", value=2.0)
    tolerance = float(st.text_input("Select the tolerance for the calculation:", value=1e-6))

    if st.button("Calculate"):
        x = symbols('x')
        try:
            f_expr = sympify(user_function)  # Converts the user input into a symbolic expression
            f = lambdify(x, f_expr, 'numpy')  # Converts the symbolic expression to a lambda function for evaluation
            
            result, message = false_position(f, a, b, tol=tolerance)
            if result is not None:
                # Customize DataFrame display to show more decimal places
                pd.set_option('display.float_format', lambda x: '%.10f' % x)
                print(result)
                st.dataframe(result, width=800, height=400)
                
                # Plot the table columns
                st.write("The root of the function is approximately:", result.iloc[-1]["X"])
                chart_data = result[["a", "b", "X", "f(x)", "Error"]]
                st.line_chart(chart_data)
                                
            else:
                st.error(message)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
