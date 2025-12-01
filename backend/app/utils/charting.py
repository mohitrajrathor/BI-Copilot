import matplotlib.pyplot as plt
import io
import base64

def generate_chart(df, chart_type="bar", x_col=None, y_col=None, title="Chart"):
    plt.figure(figsize=(10, 6))
    
    if chart_type == "bar":
        if x_col and y_col:
            plt.bar(df[x_col], df[y_col])
            plt.xlabel(x_col)
            plt.ylabel(y_col)
    elif chart_type == "line":
        if x_col and y_col:
            plt.plot(df[x_col], df[y_col])
            plt.xlabel(x_col)
            plt.ylabel(y_col)
    elif chart_type == "scatter":
        if x_col and y_col:
            plt.scatter(df[x_col], df[y_col])
            plt.xlabel(x_col)
            plt.ylabel(y_col)
    elif chart_type == "pie":
        if y_col:
            plt.pie(df[y_col], labels=df[x_col] if x_col else None, autopct='%1.1f%%')
    
    plt.title(title)
    plt.tight_layout()
    
    # Save to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    
    graphic = base64.b64encode(image_png)
    return graphic.decode('utf-8')
