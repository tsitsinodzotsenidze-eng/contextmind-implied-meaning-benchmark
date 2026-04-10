import textwrap
import re
import kaggle_benchmarks as kbench


def extract_choice(response: str) -> str:
    """
    Extract a single answer choice (A-D) from model output.
    Priority:
    1) boxed answer: \\boxed{A}
    2) explicit final-answer phrases
    3) last standalone A-D near the end
    """
    if not isinstance(response, str):
        return ""

    text = response.strip()

    # 1) \boxed{A}
    m = re.search(r"\\boxed\{\s*([A-D])\s*\}", text, flags=re.IGNORECASE)
    if m:
        return m.group(1).upper()

    # 2) Explicit final-answer phrases
    patterns = [
        r"(?:final answer|answer is|best answer is|correct answer is)\s*[:\-]?\s*\(?\s*([A-D])\s*\)?",
        r"(?:therefore|thus|so)\s*,?\s*(?:the )?(?:answer|best answer)\s*(?:is)?\s*[:\-]?\s*\(?\s*([A-D])\s*\)?",
        r"^\s*([A-D])\s*$",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            return m.group(1).upper()

    # 3) Last standalone A-D near the end
    tail = text[-200:]
    matches = re.findall(r"\b([A-D])\b", tail, flags=re.IGNORECASE)
    if matches:
        return matches[-1].upper()

    return ""


@kbench.task(
    name="indirect_geoeconomic_intent",
    description="Identify hidden geoeconomic concerns or strategic aims conveyed through neutral institutional language."
)
def indirect_geoeconomic_intent(llm) -> None:
    cases = [
        {
            "prompt": textwrap.dedent("""
                Context:
                A finance minister is discussing industrial resilience after a regional economic meeting.

                Statement:
                "In sectors where continuity matters, procurement frameworks should reward redundancy rather than concentration."

                Question:
                What is the speaker most likely trying to achieve?

                A. Lower procurement costs by encouraging firms to concentrate orders through the most efficient single foreign supplier
                B. Reduce the risk that disruptions affecting a narrow supplier base could impair continuity in critical sectors
                C. Encourage firms to diversify sourcing mainly to improve routine market flexibility and price adjustment capacity
                D. Increase public oversight of procurement in sectors where concentrated supplier dependence could create strategic exposure

                Answer with only A, B, C, or D.
            """).strip(),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                At a regional monetary forum, a central bank official discusses options for cross-border trade settlement.

                Statement:
                "For a limited set of transactions, it may be prudent to expand arrangements that do not require automatic routing through third-country currency channels, especially where continuity may be vulnerable to external disruption."

                Question:
                What hidden concern most plausibly motivates this statement?

                A. Improve exchange-rate signaling in order to attract more short-term portfolio inflows
                B. Expand bilateral liquidity and settlement backstops in order to reduce payment instability during periods of external financial stress
                C. Reduce exposure to external financial chokepoints created by dependence on dominant third-country currency routes
                D. Require exporters to rely primarily on domestic-currency settlement rather than routine foreign-currency invoicing

                Answer with only A, B, C, or D.
            """).strip(),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A government spokesperson comments on revised rules for foreign participation in ports and logistics hubs.

                Statement:
                "We continue to welcome long-term international capital, while ensuring that assets with systemic relevance remain subject to heightened review."

                Question:
                What hidden intent is most plausibly reflected in this statement?

                A. Commit to granting foreign investors the same approval standard regardless of asset sensitivity
                B. Reassure markets that the government intends to accelerate broader private participation in transport infrastructure
                C. Signal that foreign investors in logistics assets should expect more extensive disclosure, reporting, and procedural review before approval, even where the overall investment climate remains open
                D. Preserve a pro-investment posture while retaining case-by-case discretion over whether strategically sensitive assets receive approval

                Answer with only A, B, C, or D.
            """).strip(),
            "answer": "D",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                An industry minister is asked why new licensing requirements were introduced for exports of a mineral essential to battery production.

                Statement:
                "Where downstream production depends on continuity, it is reasonable to ensure that outbound flows do not create avoidable volatility for firms operating further along the value chain."

                Question:
                What concern is most likely operating in the background of this statement?

                A. That domestic manufacturers may face unstable access to an essential raw material they need for production
                B. That the government is trying to gain bargaining leverage over foreign buyers by controlling the pace of exports in a strategically sensitive input market
                C. That policymakers want to encourage a shift away from raw-material export dependence and toward higher-value downstream processing
                D. That unpredictable export restrictions could damage the country’s reputation as a reliable supplier in global mineral markets

                Answer with only A, B, C, or D.
            """).strip(),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A deputy trade minister explains why a new review mechanism was added to long-term telecom infrastructure contracts.

                Statement:
                "The purpose is not to slow modernization, but to ensure that infrastructure carrying strategic volumes of data does not become dependent on terms that are difficult to revise once embedded."

                Question:
                What hidden concern is most plausibly motivating this statement?

                A. That the priority is to increase competition by making it easier for low-cost vendors to enter quickly
                B. That long-term dependence on hard-to-reverse foreign infrastructure arrangements could create strategic vulnerability
                C. That future upgrades and follow-on contracts should not leave domestic operators with too little room to negotiate or compete once core systems are embedded
                D. That strategically sensitive cross-border data flows may need tighter routing, access, or continuity controls during periods of elevated risk

                Answer with only A, B, C, or D.
            """).strip(),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A cabinet official defends new incentives for domestic pharmaceutical ingredient production.

                Statement:
                "The measure is not designed to displace trade, but to ensure that basic therapeutic supply is not overly exposed to disruptions originating outside the region."

                Question:
                What strategic concern most plausibly lies behind this statement?

                A. That the government wants stronger leverage to negotiate more stable long-term prices from foreign suppliers of critical pharmaceutical inputs
                B. That policymakers want to shift the sector toward higher-value domestic pharmaceutical processing rather than continued reliance on imported ingredients
                C. That short-run resilience depends mainly on preserving the ability to scale up emergency imports of finished medicines during external shocks
                D. That excessive dependence on external sources of essential inputs could endanger continuity of basic medical supply

                Answer with only A, B, C, or D.
            """).strip(),
            "answer": "D",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                At a parliamentary hearing, an energy minister is asked why gas storage policy now includes stronger diversification targets.

                Statement:
                "Where seasonal stability matters, resilience is improved when no single external source is positioned to convert temporary strain into bargaining leverage."

                Question:
                What hidden intent is most plausibly reflected in this statement?

                A. Increase reliance on one large supplier in exchange for more favorable spot prices
                B. Build additional flexibility into procurement and storage planning so that temporary external shortages do not sharply weaken the government’s negotiating position
                C. Reduce the risk that reliance on one outside supplier could be used for political or commercial pressure
                D. Reduce exposure to imported energy by accelerating substitution where feasible, even if this raises short-term costs

                Answer with only A, B, C, or D.
            """).strip(),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A senior official discusses a proposal to expand domestic cloud procurement standards for public agencies.

                Statement:
                "In environments where continuity of governance depends on uninterrupted digital access, procurement cannot remain indifferent to recoverability and jurisdictional control."

                Question:
                What hidden concern is most plausibly motivating this statement?

                A. That digital public services may become strategically fragile if critical systems are hosted under external legal or technical control
                B. That procurement standards should give public agencies stronger leverage to demand clearer recovery, audit, and data-access guarantees from major cloud vendors
                C. That procurement can be used to strengthen longer-term domestic public-sector digital capability and reduce habitual dependence on externally governed infrastructure
                D. That public cloud contracts should contain stronger continuity, recovery, and portability safeguards for periods of cross-border legal or regulatory conflict

                Answer with only A, B, C, or D.
            """).strip(),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                During a discussion on food security, an agriculture minister comments on grain reserve policy.

                Statement:
                "Open markets remain indispensable, but resilience improves when temporary interruptions abroad do not immediately translate into domestic vulnerability."

                Question:
                What strategic intent is most plausibly implied by this statement?

                A. Use reserve policy mainly to reduce domestic food-price volatility during periods of global grain market stress
                B. Reduce reliance on emergency spot purchases by securing more predictable access to imported grain during external disruptions
                C. Reduce longer-term food-security risk by lowering structural dependence on imported feed and grain-intensive consumption during prolonged external disruption
                D. Preserve openness while building buffer capacity against externally generated supply disruptions in essential food markets

                Answer with only A, B, C, or D.
            """).strip(),
            "answer": "D",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A strategic industries adviser explains why new screening criteria were added to semiconductor joint ventures.

                Statement:
                "Partnerships remain welcome, provided they do not leave essential upgrading capacity contingent on decisions taken entirely beyond our policy reach."

                Question:
                What hidden concern most plausibly motivates this statement?

                A. That screening should ensure joint ventures preserve domestic influence over upgrade sequencing, technology transfer, and future investment commitments in strategically important technologies
                B. That semiconductor policy should place greater emphasis on building domestic commercial and managerial capability alongside technical collaboration
                C. That crucial technological progress should not become fully dependent on actors outside domestic policy influence
                D. That semiconductor strategy should tolerate deeper reliance on external design ecosystems so long as partnership inflows remain strong

                Answer with only A, B, C, or D.
            """).strip(),
            "answer": "C",
        },
    ]

    for i, case in enumerate(cases, start=1):
        response = llm.prompt(case["prompt"])
        pred = extract_choice(response)

        assert pred == case["answer"], (
            f"Item {i} failed. Expected {case['answer']}, got {pred}. "
            f"Raw response: {response}"
        )
