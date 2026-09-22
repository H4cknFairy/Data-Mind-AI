def detect_chart_type(question: str) -> str:

    q = question.lower().strip()


    # =====================================================
    # REVENUE BY REGION
    # =====================================================

    if (
        "revenue by region" in q
        or "sales by region" in q
        or "region revenue" in q
        or "revenue across regions" in q
        or "regional revenue" in q
        or "revenue for each region" in q
        or "revenue in each region" in q
        or "compare regions" in q
        or "compare sales across regions" in q
        or "which region" in q
    ):

        return "revenue_region"


    # =====================================================
    # REVENUE BY PRODUCT
    # =====================================================

    if (
        "revenue by product" in q
        or "sales by product" in q
        or "product revenue" in q
        or "products by revenue" in q
        or "top products" in q
        or "highest revenue products" in q
    ):

        return "revenue_product"


    # =====================================================
    # QUANTITY BY PRODUCT
    # =====================================================

    if (
        "quantity by product" in q
        or "units by product" in q
        or "products sold" in q
        or "sell the most" in q
        or "sold the most" in q
        or "most units" in q
    ):

        return "quantity_product"


    # =====================================================
    # DISCOUNT VS REVENUE
    # =====================================================

    if (
        "discount" in q
        and "revenue" in q
    ):

        return "discount_revenue"


    # =====================================================
    # REVENUE DISTRIBUTION
    # =====================================================

    if (
        "revenue distribution" in q
        or "distribution of revenue" in q
        or "revenue spread" in q
        or "distribution of sales" in q
    ):

        return "revenue_distribution"


    # =====================================================
    # NO CHART
    # =====================================================

    return "none"