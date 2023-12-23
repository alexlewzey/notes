# DBSCAN hyperparameter tuning
eps_range = [0.5, 1]
min_samples_range = [5, 10]
grid = list(itertools.product(eps_range, min_samples_range))

scores_dbscan = []
for eps, min_samples in tqdm(grid):
    labels_ = (
        cluster.DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1).fit(x_umap).labels_
    )
    x[f"cluster_umap_dbscan_eps_{eps}_min_samples_{min_samples}"] = labels_.astype(str)
    try:
        score = metrics.silhouette_score(x_umap, labels_)
    except ValueError:
        print(f"error: {eps}, {min_samples}")
    scores_dbscan.append({"eps": eps, "min_samples": min_samples, "score": score})

scores_dbscan = pd.DataFrame(scores_dbscan)


pt = (
    scores_dbscan.sort_values(["eps", "min_samples"])
    .groupby(["eps", "min_samples"])["score"]
    .mean()
    .unstack()
)
fig = px_contour(pt)
display_plotly(fig)
