import plotly.graph_objects as go
import json

class AllocationVisualizer:
    @staticmethod
    def create_pie_chart(allocation, risk_profile):
        """Create an interactive pie chart using Plotly"""
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        fig = go.Figure(data=[go.Pie(
            labels=list(allocation.keys()),
            values=list(allocation.values()),
            hole=.3,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=14),
            hovertemplate="<b>%{label}</b><br>" +
                         "Allocation: %{value}%<br>" +
                         "<extra></extra>"
        )])

        fig.update_layout(
            title={
                'text': f'Asset Allocation for {risk_profile} Risk Profile',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20)
            },
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=100, l=20, r=20, b=100)
        )

        # Return both the figure and its JSON representation
        return {
            'figure': fig,
            'json': json.dumps(fig.to_dict()),
            'div': fig.to_html(full_html=False)
        }

    @staticmethod
    def create_profile_visualization(profile_data):
        """Create visualization of risk profile data"""
        # This could be expanded to create additional visualizations
        # of the risk profile data
        pass