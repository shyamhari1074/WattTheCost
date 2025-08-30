import streamlit as st
import plotly.express as px

def calculate_ev_tco(
    purchase_price: float,
    per_charge_range: float,
    charges_per_year: int,
    car_efficiency_kwh: float,
    ownership_years: int,
    electricity_cost_inr: float,
    public_charging_cost_inr: float,
    charging_split_percent: float,
    tax_credit_inr: float,
    insurance_cost_per_year: float,
    maintenance_cost_per_year: float,
) -> dict:
    if car_efficiency_kwh <= 0:
        raise ValueError("Car efficiency must be greater than 0 km/kWh.")

    annual_mileage = per_charge_range * charges_per_year
    home_charging_ratio = charging_split_percent / 100.0

    initial_cost = purchase_price - tax_credit_inr
    total_kwh = (annual_mileage * ownership_years) / car_efficiency_kwh
    avg_charging_cost = (
        electricity_cost_inr * home_charging_ratio
        + public_charging_cost_inr * (1 - home_charging_ratio)
    )
    total_charging_cost = total_kwh * avg_charging_cost
    total_maintenance_cost = maintenance_cost_per_year * ownership_years
    total_insurance_cost = insurance_cost_per_year * ownership_years

    total_tco = (
        initial_cost + total_charging_cost
        + total_maintenance_cost + total_insurance_cost
    )

    return {
        "Initial Cost": initial_cost,
        "Charging Cost": total_charging_cost,
        "Maintenance Cost": total_maintenance_cost,
        "Insurance Cost": total_insurance_cost,
        "Total TCO": total_tco,
        "Estimated Annual Mileage": annual_mileage,
    }


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="EV TCO Calculator", layout="wide")
st.title("🔋 EV Total Cost of Ownership (TCO) Calculator")

with st.sidebar:
    st.header("⚙️ Customize Inputs")
    years = st.slider("Ownership Duration (Years)", 1, 15, 5)
    purchase_price = st.number_input("Purchase Price (₹)", 0, 1_00_00_000, 20_00_000)
    per_charge_range = st.number_input("Range per Full Charge (km)", 50, 1000, 300)
    charges_per_year = st.number_input("Full Charges per Year", 0, 1000, 200)
    car_efficiency_kwh = st.number_input("Efficiency (km/kWh)", 1.0, 20.0, 7.0)
    electricity_cost_inr = st.number_input("Home Electricity (₹/kWh)", 0.0, 50.0, 8.0)
    public_charging_cost_inr = st.number_input("Public Charging (₹/kWh)", 0.0, 100.0, 20.0)
    charging_split_percent = st.slider("Home Charging %", 0, 100, 70)
    tax_credit_inr = st.number_input("Tax Credit (₹)", 0, 5_00_000, 0)
    insurance_cost_per_year = st.number_input("Insurance per Year (₹)", 0, 1_00_000, 30_000)
    maintenance_cost_per_year = st.number_input("Maintenance per Year (₹)", 0, 1_00_000, 10_000)

if st.button("💡 Calculate TCO", use_container_width=True):
    result = calculate_ev_tco(
        purchase_price, per_charge_range, charges_per_year, car_efficiency_kwh, years,
        electricity_cost_inr, public_charging_cost_inr, charging_split_percent,
        tax_credit_inr, insurance_cost_per_year, maintenance_cost_per_year
    )

    st.subheader("📊 Results Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total TCO", f"₹ {result['Total TCO']:,.0f}")
    col2.metric("Annual Mileage", f"{result['Estimated Annual Mileage']:,.0f} km")
    col3.metric("Charging Cost", f"₹ {result['Charging Cost']:,.0f}")

    # Pie Chart
    cost_breakdown = {
        "Initial Cost": result["Initial Cost"],
        "Charging Cost": result["Charging Cost"],
        "Maintenance Cost": result["Maintenance Cost"],
        "Insurance Cost": result["Insurance Cost"],
    }
    fig = px.pie(
        values=cost_breakdown.values(),
        names=cost_breakdown.keys(),
        title="Cost Breakdown",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("🔎 Detailed Breakdown"):
        for k, v in result.items():
            if k != "Estimated Annual Mileage":
                st.write(f"**{k}:** ₹ {v:,.0f}")

# ---- Custom Styling ----
# Custom CSS
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(to right, #1c1c1c, #0f2027);
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    .stButton>button {
        background-color: #27ae60;
        color: white;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2ecc71;
        transform: scale(1.05);
    }
    .stMetric {
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)

