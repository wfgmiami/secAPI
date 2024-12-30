from QuantLib import *

today = Date(24, December, 2024)
Settings.instance().evaluationDate = today

option = EuropeanOption(
    PlainVanillaPayoff(Option.Call, 100.0), EuropeanExercise(Date(24, March, 2025))
)

u = SimpleQuote(100.0)
r = SimpleQuote(0.01)
sigma = SimpleQuote(0.20)

riskFreeCurve = FlatForward(0, TARGET(), QuoteHandle(r), Actual360())
volatility = BlackConstantVol(0, TARGET(), QuoteHandle(sigma), Actual360())

process = BlackScholesProcess(
    QuoteHandle(u),
    YieldTermStructureHandle(riskFreeCurve),
    BlackVolTermStructureHandle(volatility),
)

engine = AnalyticEuropeanEngine(process)

option.setPricingEngine(engine)

print(option.NPV())
print(option.delta())
print(option.gamma())
print(option.vega())
