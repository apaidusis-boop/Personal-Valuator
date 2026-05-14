---
type: rag_research
qid: damodaran_option_pricing
date: 2026-04-24
book_filter: investment_valuation
tags: [rag, research, overnight]
---

# damodaran_option_pricing

**Question**: Black-Scholes e real options em valuation — quando Damodaran sugere usar?

**Book filter**: `investment_valuation`
**Generated in**: 8.3s by Qwen 14B + nomic-embed (100% local, 0 Claude tokens)

## Answer

Based on the provided excerpts from "Investment Valuation" by Aswath Damodaran, there is no specific mention of when Damodaran suggests using Black-Scholes versus real options in valuation. However, several insights can be derived regarding their application:

1. **Black-Scholes Model**: The model is primarily used for valuing financial options with clearly defined exercise prices and maturities on underlying assets that are traded [book:chunk 0123.txt]. It provides a robust framework for estimating the value of any option using five key variables, including the current asset price (S), strike price (K), time to expiration (t), riskless interest rate (r), and variance in the natural logarithm of the underlying asset's value (σ²) [book:chunk 0109.txt].

2. **Real Options**: These are options on real assets rather than financial ones, often taking more complicated forms with limits on potential upside or knockout provisions [book:chunk 0123.txt]. Real options can include capped and barrier options, compound options (where an option is derived from another option), and rainbow options where uncertainty involves multiple underlying assets [book:chunk 0124.txt].

Damodaran discusses the limitations of applying Black-Scholes to real options due to the non-traded nature of real assets and the complexity introduced by sequential or compound options. He suggests that while it is possible to modify Black-Scholes models for these complexities, doing so may introduce significant estimation errors [book:chunk 0860.txt]. Therefore, he recommends using conservative estimates with simple valuation models as a floor on the value of real options rather than overcomplicating the model.

In summary, Damodaran does not provide a specific recommendation in the given excerpts for when to use Black-Scholes versus real options. However, it is implied that Black-Scholes is more suitable for financial assets with clear exercise terms and traded underlying assets, whereas real options are necessary for valuing decisions involving real assets where uncertainty and flexibility play significant roles [book:chunk 0123.txt].